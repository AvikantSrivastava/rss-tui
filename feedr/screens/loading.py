from feedr import config
from feedr.screens.base_screen import BaseScreen
from feedr.services.fetch import fetch_feeds
from textual.app import ComposeResult
from textual.containers import Center
from textual.widgets import LoadingIndicator, Static


class LoadingScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        with Center():
            yield Static("Refreshing feeds...")
            yield LoadingIndicator()

    def on_mount(self) -> None:
        self.run_worker(self._do_refresh())

    async def _do_refresh(self) -> None:
        await fetch_feeds(config.feeds)
        self.dismiss()
