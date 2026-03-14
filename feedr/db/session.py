from email.utils import parsedate_to_datetime

from sqlalchemy import and_, create_engine
from sqlalchemy.orm import sessionmaker

from feedr.constants import DB_PATH
from feedr.db.models import Article, Base, Feed

engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def add_articles_to_db(article: dict, feed_name: str, feed_url: str) -> None:
    """
    Inserts an article into the database, creating the parent feed if needed.
    Skips insertion if the article URL already exists.

    article format:
    {'url': 'https://...', 'title': '...', 'published': 'Fri, 13 Mar 2026 17:51:34 +0000', 'summary': '...'}
    """
    with session() as db:
        feed = db.query(Feed).filter_by(name=feed_name).first()
        if not feed:
            feed = Feed(name=feed_name, url=feed_url)
            db.add(feed)
            db.flush()

        exists = (
            db.query(Article)
            .filter(and_(Article.url == article["url"], Article.feed_id == feed.id))
            .first()
        )
        if not exists:
            db.add(
                Article(
                    title=article["title"],
                    published_date=article["published_date"],
                    description=article["summary"],
                    url=article["url"],
                    feed_id=feed.id,
                )
            )

        db.commit()
