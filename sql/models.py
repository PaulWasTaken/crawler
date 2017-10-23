from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class UrlData(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sourced_url_hash = Column(Integer, unique=True, nullable=False)
    url = Column(String, nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
