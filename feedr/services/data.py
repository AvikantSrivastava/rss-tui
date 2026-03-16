from feedr.db.models import Article, Feed
from feedr.db.session import session


def get_feed_data():

    data = {}

    with session() as db:
        feeds = db.query(Feed).all()

        for feed in feeds:
            articles = (
                db.query(Article)
                .filter_by(feed_id=feed.id)
                .order_by(Article.published_date.desc())
                .all()
            )
            data[feed.name] = {}

            for article in articles:
                article_key = f"article-{article.id}"
                data[feed.name][article_key] = {
                    "id": article.id,
                    "feed_id": feed.id,
                    "title": article.title,
                    "description": article.description,
                    "read": article.read or False,
                }

    return data


def mark_article_read(article_id):

    with session() as db:
        article = db.query(Article).filter_by(id=article_id).first()
        if article:
            article.read = True
            db.commit()
