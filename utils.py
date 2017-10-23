from aiohttp import ClientConnectorSSLError
from config.log import get_logger
from lxml import html
from sys import exc_info
logger = get_logger(__file__)


class UnwantedContentType(Exception):
    pass


def error_processor(url):
    error = exc_info()
    type_ = error[0]
    if type_ is AssertionError:
        logger.error("Request for %s returned non 200 code." % url)
    elif type_ is ClientConnectorSSLError:
        logger.warning("Could not establish ssl connection with %s" % url)
    elif type_ is UnwantedContentType:
        logger.warning("%s is not html file." % url)
    else:
        logger.error("Got unknown exception: %s" % error[1])


async def fetch(url, session):
    async with session.get(url) as response:
        assert response.status == 200
        if response.content_type == "text/html":
            return await response.text()
        raise UnwantedContentType


async def process_response(content, extract_links):
    html_obj = html.fromstring(content)

    title = html_obj.xpath('//title')[0].text

    links = set()
    if extract_links:
        for link in html_obj.xpath('//a/@href'):
            if link.startswith((u'http://', u'https://')):
                links.add(link)

    return title, links


def exception_handler(loop, context):
    msg = "Message: %s. " % context.get("message", None) \
        if "message" in context else ""
    exception = "Exception: %s." % context.get("exception", None) \
        if "exception" in context else ""
    logging.error("Error occurred. " + msg + exception)
