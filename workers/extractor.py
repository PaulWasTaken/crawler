from config.log import get_logger, SIMPLE
from sql.creator import get_session
from sql.models import UrlData
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
        session = get_session()
        needed_hash = get_url_hash(self.source_url)
        query = session.query(UrlData.url, UrlData.title) \
            .filter(UrlData.source_url_hash == needed_hash) \
            .limit(self.amount)
        records = query.all()
        if records:
            for url, title in records:
                logger.info("%s: '%s'" % (url, title))
        else:
            logger.info("No data associated with url %s" % self.source_url)
        session.close()
