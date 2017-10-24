from config.log import get_logger
from sql.creator import get_engine
from sql.models import UrlData, Content
from sql.sqla import sa
logger = get_logger(__file__)


class Storage:
    def __init__(self):
        self.content = []
        self.url_data = []

    def add(self, url_record, content):
        assert isinstance(url_record, dict) and isinstance(content, dict)
        for key, value in url_record.items():
            if value is None:
                logger.error("Got empty %s for %s" %
                             (str(key), url_record.get("url")))
                return
        self.content.append(content)
        self.url_data.append(url_record)

    def flush(self):
        with get_engine().connect() as conn:
            conn.execute(sa.replace(UrlData).values(self.url_data))
            conn.execute(sa.replace(Content).values(self.content))
        self.content = []
        self.url_data = []
