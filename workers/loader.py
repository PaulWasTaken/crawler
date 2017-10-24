import config

from aiohttp import ClientSession, TCPConnector
from asyncio import ensure_future, gather, get_event_loop, Semaphore
from config.log import get_logger
from tools.utils import form_content_record, form_url_record, process_url, \
    loop_exception_handler
from workers.abstract_worker import AbstractWorker
from workers.storage import Storage

logger = get_logger(__file__)


class Loader(AbstractWorker):
    def __init__(self, source_url, loop=None, **kwargs):
        self.source_url = source_url
        self.current_urls = {source_url}
        self.storage = Storage()
        self.timeout = kwargs.get("timeout")
        self.depth = kwargs.get("depth")
        self.visited_urls = set()

        if loop is None:
            self.loop = get_event_loop()
            self.loop.set_exception_handler(loop_exception_handler)
        else:
            self.loop = loop

    def run(self):
        try:
            self.loop.run_until_complete(self.load_urls())
        except KeyboardInterrupt:
            self.loop.stop()
            self.loop.close()

    async def load_urls(self):
        con = TCPConnector(verify_ssl=config.VERIFY_SSL)
        sem = Semaphore(100)
        async with ClientSession(connector=con, conn_timeout=self.timeout) \
                as session:
            while self.depth >= 0:
                tasks = []
                for url in self.current_urls - self.visited_urls:
                    self.visited_urls.add(url)
                    tasks.append(ensure_future(
                        process_url(sem, url, session, self.depth != 0)))

                res = await gather(*tasks)

                self.update_state(res)

    def update_state(self, res):
        self.current_urls = set()
        for elem in res:
            if elem:
                self.current_urls |= elem.links
                content_record = form_content_record(elem.url, elem.content)
                url_record = form_url_record(
                    self.source_url, elem.url, elem.title)
                self.storage.add(url_record, content_record)
        self.depth -= 1
        self.storage.flush()
