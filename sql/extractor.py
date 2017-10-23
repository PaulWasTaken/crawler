import sqlalchemy as sa

from sql.creator import get_engine
from sql.models import UrlData


def extract_values(hash_, **kwargs):
    engine = get_engine()
    query = sa.select([UrlData.title], UrlData.sourced_url_hash == hash_)
    return engine.execute(query)
