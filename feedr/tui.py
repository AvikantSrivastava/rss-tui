from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from .screens.main import MainScreen
from .screens.setup import SetupScreen
from .utils import check_config_file


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
    ]

    def compose(self) -> ComposeResult:
        self.title = "RSS TUI"
        self.sub_title = "A simple RSS reader developed by Avikant"

        yield Header(show_clock=True)
        yield Footer()

    def on_mount(self):

        if check_config_file():
            self.push_screen("main")
        else:
            self.push_screen("setup")

    def action_toggle_dark(self):
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
