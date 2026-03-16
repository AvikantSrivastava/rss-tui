import asyncio
import calendar
from datetime import datetime, timezone

import feedparser
from feedctl.db.session import add_articles_to_db


def fetch(feed: dict):
    url = feed["url"]
    d = feedparser.parse(url)
    for entry in d.entries:
        yield {
            "url": entry.link,
            "title": entry.title,
            "published_date": datetime.fromtimestamp(
                calendar.timegm(entry.updated_parsed), tz=timezone.utc
            ),
            "summary": entry.summary,
            "base_url": feed["url"],
        }


def _fetch_and_write(feed: dict) -> None:
    """Blocking fetch + DB write — runs in a thread."""
    articles = fetch(feed)
    write_to_db(articles, feed["name"], feed["url"])


async def fetch_feeds(feeds: list[dict]):
    for feed in feeds:
        await asyncio.to_thread(_fetch_and_write, feed)


def write_to_db(articles, feed_name, feed_url):
    for article in articles:
        add_articles_to_db(article, feed_name, feed_url)
