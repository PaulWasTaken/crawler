from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()


class UrlData(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_url_hash = Column(Integer, nullable=False)
    url_hash = Column(Integer, unique=True, nullable=False)
    url = Column(String, nullable=False)
    title = Column(Text, nullable=False)

    content = relationship("Content", backref="urls")


class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    url_hash = Column(Integer, ForeignKey(UrlData.url_hash), nullable=False)
