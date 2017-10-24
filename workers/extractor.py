from sql.creator import get_session
from sql.models import UrlData
from tools.utils import get_url_hash
from workers.abstract_worker import AbstractWorker


class Extractor(AbstractWorker):
    def __init__(self, url, **kwargs):
        self.source_url = url
        self.amount = kwargs.get("n")

    def run(self):
        self.extract_records()

    def extract_records(self):
        session = get_session()
        query = session.query(UrlData.url, UrlData.title) \
            .filter(UrlData.source_url_hash == get_url_hash(self.source_url)) \
            .limit(self.amount)
        records = query.all()
        if records:
            for url, title in records:
                print("%s: '%s'" % (url, title))
        else:
            print("No data associated with url %s" % self.source_url)
        session.close()
