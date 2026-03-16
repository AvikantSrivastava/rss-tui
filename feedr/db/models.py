from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    url = Column(String, nullable=False)


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    published_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)


class SchemaVersion(Base):
    __tablename__ = "schema_version"

    version = Column(Integer, primary_key=True)
