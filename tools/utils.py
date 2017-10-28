try:
    from aiohttp import ClientConnectorSSLError as SslError
except ImportError:
    from aiohttp import ClientConnectorError as SslError
from aiohttp import ServerTimeoutError, ServerDisconnectedError
from collections import namedtuple
from config.log import get_logger
from hashlib import md5
from lxml import html
from sys import exc_info
from tools.exceptions import UnwantedContentType, BadReturnCode, Retry

logger = get_logger(__file__)
ResultInfo = namedtuple("ResultInfo", "url title content")
LogInfo = namedtuple("LogInfo", "method message")


async def process_url(sem, storage, url, session, extract_links):
    retries = 2
    while retries > 0:
        try:
            async with sem:
                content = await fetch(url, session)
            title, links = process_response(content, extract_links)
            storage.add(ResultInfo(url, title, content))
            return links
        except (ServerDisconnectedError, Retry):
            logger.debug("Retrying for %s." % url)
            retries -= 1
        except Exception:
            error_processor(url)
            break


EXCEPTION_LOGINFO = {
    BadReturnCode: LogInfo(logger.debug,
                           "Request for {} returned non 200 code."),
    SslError: LogInfo(logger.warning,
                      "Could not establish ssl connection with {}."),
    UnwantedContentType: LogInfo(logger.debug, "{} is not html file."),
    IndexError: LogInfo(logger.debug, "No title for url {}."),
    ServerTimeoutError: LogInfo(logger.debug, "No content from {}.")
}
DEFAULT = LogInfo(logger.error, "Got unknown exception: {} {} for url {}.")


def error_processor(url):
    error = exc_info()
    type_ = error[0]
    info = EXCEPTION_LOGINFO.get(type_, DEFAULT)
    if info is DEFAULT:
        info.method(info.message.format(*[type_, error[1], url]))
    else:
        info.method(info.message.format(*[url]))


HTTP_STATUS_CODES_TO_RETRY = [500, 502, 503, 504]


async def fetch(url, session):
    async with session.get(url) as response:
        if response.status in HTTP_STATUS_CODES_TO_RETRY:
            raise Retry
        if response.status != 200:
            raise BadReturnCode
        if response.content_type != "text/html":
            raise UnwantedContentType
        return await response.text()


def process_response(content, extract_links):
    if content[:5] == "<?xml":
        from re import sub
        content = sub("^<\?xml.+\?>", "", content)
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
