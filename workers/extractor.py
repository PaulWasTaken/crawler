from config.log import get_logger, SIMPLE
from sql.creator import get_engine
from sql.models import UrlData
from sqlalchemy import select
from tools.utils import get_url_hash
from workers.abstract_worker import AbstractWorker

logger = get_logger(__name__, SIMPLE)


class Extractor(AbstractWorker):
    def __init__(self, url, **kwargs):
        self.source_url = url
        self.amount = kwargs.get("n")

    def run(self):
        self.extract_records()

    def extract_records(self):
        needed_hash = get_url_hash(self.source_url)
        with get_engine().connect() as conn:
            where = UrlData.source_url_hash == needed_hash
            query = select([UrlData.url, UrlData.title], where)\
                .limit(self.amount)
            records = conn.execute(query).fetchall()
            if records:
                for url, title in records:
                    logger.info("%s : '%s'" % (url, title))
            else:
                logger.info("No data associated with url %s" % self.source_url)
