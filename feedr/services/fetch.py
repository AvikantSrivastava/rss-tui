import calendar
from datetime import datetime, timezone

import feedparser
from feedr.config import Config
from feedr.db.session import add_articles_to_db


def fetch(feed: dict):
    url = feed["url"]
    d = feedparser.parse(url)
    for entry in d.entries:
        yield {
            "url": entry.link,
            "title": entry.title,
            "published_date": datetime.fromtimestamp(
                calendar.timegm(entry.published_parsed), tz=timezone.utc
            ),
            "summary": entry.summary,
            "base_url": feed["url"],
        }


async def fetch_feeds(feeds: list[dict]):
    for feed in feeds:
        d = fetch(feed)
        write_to_db(d, feed["name"], feed["url"])


def write_to_db(articles, feed_name, feed_url):
    for article in articles:
        add_articles_to_db(article, feed_name, feed_url)
