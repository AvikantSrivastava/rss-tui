from feedctl import config
from feedctl.services.fetch import fetch_feeds


async def refresh_feeds() -> None:
    """Fetch and refresh all RSS feed data."""
    await fetch_feeds(config.feeds)
