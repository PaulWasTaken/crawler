try:
    from aiohttp import ClientConnectorSSLError as SslError
except ImportError:
    from aiohttp import ClientConnectorError as SslError
from collections import namedtuple
from config.log import get_logger
from hashlib import md5
from lxml import html
from sys import exc_info
from tools.exceptions import UnwantedContentType, BadReturnCode

logger = get_logger(__file__)
ResultInfo = namedtuple("ResultInfo", "url title content")


async def process_url(sem, storage, url, session, extract_links):
    try:
        async with sem:
            logger.debug("Downloading url %s" % url)
            content = await fetch(url, session)
        title, links = process_response(content, extract_links)
        storage.add(ResultInfo(url, title, content))
        return links
    except Exception:
        error_processor(url)


def error_processor(url):
    error = exc_info()
    type_ = error[0]
    if type_ is BadReturnCode:
        logger.error("Request for %s returned non 200 code." % url)
    elif type_ is SslError:
        logger.warning("Could not establish ssl connection with %s" % url)
    elif type_ is UnwantedContentType:
        logger.warning("%s is not html file." % url)
    elif type_ is IndexError:
        logger.error("No title for url %s" % url)
    else:
        logger.error("Got unknown exception: %s %s" % (type_, error[1]))


async def fetch(url, session):
    async with session.get(url) as response:
        if response.status != 200:
            raise BadReturnCode
        if response.content_type != "text/html":
            raise UnwantedContentType
        return await response.text()


def process_response(content, extract_links):
    html_obj = html.fromstring(content)

    title = html_obj.xpath('//title')[0].text

    if not title:
        title = "Empty title(literally)."

    links = set()
    if extract_links:
        for link in html_obj.xpath('//a/@href'):
            if link.startswith((u'http://', u'https://')):
                links.add(link)

    return title, links


def form_url_record(source_url, url, title):
    return {
        "source_url_hash": get_url_hash(source_url),
        "url_hash": get_url_hash(url),
        "title": title,
        "url": url
    }


def form_content_record(url, content):
    return {
        "content": content,
        "url_hash": get_url_hash(url)
    }


def get_url_hash(url):
    return md5(url.encode('utf-8')).hexdigest()[:16]


def loop_exception_handler(loop, context):
    msg = "Message: %s. " % context.get("message") \
        if "message" in context else ""
    exception = "Exception: %s." % context.get("exception") \
        if "exception" in context else ""
    logger.error("Error occurred. " + msg + exception)
