import config

from aiohttp import ClientSession, TCPConnector
from asyncio import ensure_future, gather, get_event_loop, Semaphore
from config.log import get_logger
from tools.utils import process_url, loop_exception_handler
from workers.abstract_worker import AbstractWorker
from workers.storage import Storage

logger = get_logger(__file__)


class Loader(AbstractWorker):
    def __init__(self, source_url, loop=None, **kwargs):
        self.source_url = source_url
        self.current_urls = {source_url}
        self.storage = Storage(source_url)
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
                urls = self.current_urls - self.visited_urls
                logger.debug("Got %s at %s run." % (len(urls), self.depth))
                for url in urls:
                    self.visited_urls.add(url)
                    tasks.append(ensure_future(
                        process_url(sem, self.storage,
                                    url, session, self.depth != 0)))

                links = await gather(*tasks)

                self.update_state(links)

        self.storage.flush()

    def update_state(self, links):
        self.current_urls = set()
        for elem in links:
            if elem:
                self.current_urls |= elem
        self.depth -= 1
