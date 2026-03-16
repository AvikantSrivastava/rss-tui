from feedr.db.session import session
from feedr.db.models import Feed, Article


def get_feed_data():
    
    data = {}
    
    with session() as db:
        feeds = db.query(Feed).all()

        for feed in feeds:
            articles = db.query(Article).filter_by(feed_id=feed.id).order_by(Article.published_date.desc()).all()
            data[feed.name] = {}

            for article in articles:
                article_key = f"article-{article.id}"
                data[feed.name][article_key] = {
                    "title": article.title,
                    "description": article.description,
                }

    return data