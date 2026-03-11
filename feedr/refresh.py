import asyncio


async def refresh_feeds() -> None:
    """Fetch and refresh all RSS feed data."""
    await asyncio.sleep(2)
