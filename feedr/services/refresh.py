from feedr import config
from feedr.services.fetch import fetch_feeds


async def refresh_feeds() -> None:
    """Fetch and refresh all RSS feed data."""
    await fetch_feeds(config.feeds)
