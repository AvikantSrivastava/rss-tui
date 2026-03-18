from pathlib import Path
from typing import Iterable

from textual.app import App, ComposeResult, SystemCommand
from textual.screen import Screen
from textual.widgets import Footer, Header

from feedctl.screens.loading import LoadingScreen
from feedctl.screens.main import MainScreen
from feedctl.screens.setup import SetupScreen
from feedctl.utils import check_config_file

_HERE = Path(__file__).parent


class RSSApp(App):
    CSS_PATH = _HERE / "app.tcss"
    SCREENS = {
        "main": MainScreen,
        "setup": SetupScreen,
    }

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        self.title = "RSS TUI"
        self.sub_title = "A simple RSS reader developed by Avikant"

        yield Header(show_clock=True)
        yield Footer()

    def on_mount(self):
        try:
            self.theme = "monokai"
        except Exception:
            self.theme = "textual-dark"
        if check_config_file():
            self.push_screen("main")
        else:
            self.push_screen("setup")

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    async def action_refresh(self):
        await self.push_screen(LoadingScreen())
