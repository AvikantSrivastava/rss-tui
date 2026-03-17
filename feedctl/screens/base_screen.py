from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label


class BaseScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield from self.compose_body()
        yield Footer()

    def compose_body(self) -> ComposeResult:
        yield Label("Override me")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
