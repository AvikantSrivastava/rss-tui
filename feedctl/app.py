from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from feedctl import config
from feedctl.db.session import reconcile_feeds
from feedctl.screens.cleanup import CleanupScreen
from feedctl.screens.loading import LoadingScreen
from feedctl.screens.main import MainScreen
from feedctl.screens.setup import SetupScreen
from feedctl.utils import check_config_file


class RSSApp(App):
    CSS_PATH = "./app.tcss"
    SCREENS = {
        "main": MainScreen,
        "setup": SetupScreen,
    }

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("c", "cleanup", "Clean up DB"),
    ]

    def compose(self) -> ComposeResult:
        self.title = "RSS TUI"
        self.sub_title = "A simple RSS reader developed by Avikant"

        yield Header(show_clock=True)
        yield Footer()

    def on_mount(self):
        self.theme = "monokai"
        if check_config_file():
            config.reload()
            reconcile_feeds(config.feeds)
            self.push_screen("main")
        else:
            self.push_screen("setup")

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def action_refresh(self):
        await self.push_screen(LoadingScreen())

    def action_cleanup(self):
        self.push_screen(CleanupScreen())
