from aiohttp import ClientSession, TCPConnector
from asyncio import ensure_future, gather
from collections import namedtuple
from config.log import get_logger
from utils import fetch, process_response, error_processor
ResultInfo = namedtuple("ResultInfo", "url title links content")
logger = get_logger(__file__)


async def process_url(url, session, extract_links):
    try:
        content = await fetch(url, session)
        title, links = await process_response(content, extract_links)
        logger.debug("Got %s links for url %s" % (len(links), url))
        return ResultInfo(url, title, links, content)
    except Exception:
        error_processor(url)


async def load_urls(urls, **kwargs):
    tasks = []
    timeout = kwargs.get("timeout")
    depth = kwargs.get("depth")
    visited_urls = set()
    con = TCPConnector(limit=1000, verify_ssl=False)
    async with ClientSession(connector=con, conn_timeout=timeout) \
            as session:
        while depth >= 0:
            for url in urls:
                visited_urls.add(url)
                tasks.append(ensure_future(
                    process_url(url, session, depth != 0)))

            res = await gather(*tasks)

            new_urls = set()
            for elem in res:
                if elem:
                    new_urls |= elem.links

            repeated_urls = visited_urls.intersection(new_urls)
            urls = new_urls - repeated_urls

            depth -= 1
