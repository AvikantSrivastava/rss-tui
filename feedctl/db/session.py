import logging
import os
from collections import defaultdict
from datetime import datetime, timedelta

from feedctl.constants import DB_PATH
from feedctl.db.models import Article, Base, Feed
from sqlalchemy import and_, create_engine, or_
from sqlalchemy.orm import sessionmaker

engine = create_engine(f"sqlite:///{DB_PATH}")
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)


def _migrate() -> None:
    """Bring an existing on-disk database up to the current schema.

    ``Base.metadata.create_all`` only creates missing tables; it never alters
    existing ones. So for databases created before URL-based identity we:
      1. add the ``active`` column if it is missing,
      2. merge legacy duplicate feed rows that share a URL (these were created
         by the old name-based matching when a feed was renamed in config),
      3. add a UNIQUE index on ``feeds.url``.
    """
    with engine.begin() as conn:
        cols = [
            row[1]
            for row in conn.exec_driver_sql("PRAGMA table_info(feeds)").fetchall()
        ]
        if "active" not in cols:
            conn.exec_driver_sql(
                "ALTER TABLE feeds ADD COLUMN active BOOLEAN NOT NULL DEFAULT 1"
            )

    with session() as db:
        groups: dict[str, list[Feed]] = defaultdict(list)
        for feed in db.query(Feed).order_by(Feed.id).all():
            groups[feed.url].append(feed)

        for feeds in groups.values():
            if len(feeds) <= 1:
                continue
            canonical = feeds[0]
            for dup in feeds[1:]:
                db.query(Article).filter_by(feed_id=dup.id).update(
                    {Article.feed_id: canonical.id}, synchronize_session=False
                )
                db.delete(dup)
        db.commit()

    with engine.begin() as conn:
        conn.exec_driver_sql(
            "CREATE UNIQUE INDEX IF NOT EXISTS ix_feeds_url ON feeds(url)"
        )


_migrate()


def reconcile_feeds(config_feeds: list[dict]) -> None:
    """Sync the feeds table with the current config, keyed by URL.

    For each config feed we upsert by URL: an existing row has its ``name``
    updated in place (so a rename does not create a second feed) and is marked
    active. Feeds whose URL is no longer in the config are marked inactive but
    kept, along with their articles.
    """
    config_urls = {feed["url"] for feed in config_feeds}

    with session() as db:
        for cf in config_feeds:
            feed = db.query(Feed).filter_by(url=cf["url"]).first()
            if feed is None:
                db.add(Feed(name=cf["name"], url=cf["url"], active=True))
            else:
                feed.name = cf["name"]
                feed.active = True

        for feed in db.query(Feed).all():
            if feed.url not in config_urls:
                feed.active = False

        db.commit()


def add_articles_to_db(article: dict, feed_name: str, feed_url: str) -> None:
    """
    Inserts an article into the database, creating the parent feed if needed.
    Skips insertion if the article URL already exists.

    article format:
    {'url': 'https://...', 'title': '...', 'published': 'Fri, 13 Mar 2026 17:51:34 +0000', 'summary': '...'}
    """
    with session() as db:
        feed = db.query(Feed).filter_by(url=feed_url).first()
        if not feed:
            feed = Feed(name=feed_name, url=feed_url, active=True)
            db.add(feed)
            db.flush()
        else:
            if feed.name != feed_name:
                feed.name = feed_name
            if not feed.active:
                feed.active = True

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


def get_db_size_bytes() -> int:
    """Return the size of the SQLite file on disk in bytes (0 if missing)."""
    try:
        return os.path.getsize(DB_PATH)
    except OSError:
        return 0


def cleanup_database(days: int = 30) -> int:
    """Delete old and orphaned articles, then reclaim disk space.

    Removes any article that is either older than ``days`` (across all feeds) or
    belongs to an inactive feed (one removed/renamed-away from the config). Feed
    rows themselves are always preserved. Returns the number of articles deleted.
    """
    cutoff = datetime.utcnow() - timedelta(days=days)

    with session() as db:
        inactive_ids = [
            feed.id for feed in db.query(Feed).filter_by(active=False).all()
        ]

        condition = Article.published_date < cutoff
        if inactive_ids:
            condition = or_(condition, Article.feed_id.in_(inactive_ids))

        query = db.query(Article).filter(condition)
        deleted = query.count()
        query.delete(synchronize_session=False)
        db.commit()

    # VACUUM cannot run inside a transaction; use a raw autocommit connection.
    try:
        with engine.connect() as conn:
            conn.exec_driver_sql("VACUUM")
    except Exception:  # pragma: no cover - best-effort space reclaim
        logging.warning("VACUUM failed after cleanup", exc_info=True)

    return deleted
