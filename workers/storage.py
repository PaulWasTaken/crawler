import config

from config.log import get_logger
from sql.creator import get_engine
from sql.models import UrlData, Content
from sql.sqla import sa
from tools.utils import form_content_record, form_url_record

logger = get_logger(__file__)


class Storage:
    def __init__(self, source_url, threshold):
        self.source_url = source_url
        self.content = []
        self.url_data = []
        self.size = 0
        self.threshold = threshold

    def add(self, elem):
        content_record = form_content_record(elem.url, elem.content)
        url_record = form_url_record(self.source_url, elem.url, elem.title)
        self.content.append(content_record)
        self.size += len(elem.content)
        self.url_data.append(url_record)

        if self.size > self.threshold:
            self.flush()

    def flush(self):
        with get_engine().connect() as conn:
            conn.execute(sa.replace(UrlData).values(self.url_data))
            conn.execute(sa.replace(Content).values(self.content))
        self.content.clear()
        self.size = 0
        self.url_data.clear()
        logger.debug("Storage has been successfully flushed .")
