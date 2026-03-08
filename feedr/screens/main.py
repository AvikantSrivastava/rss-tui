from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Label, OptionList, Static
from textual.widgets.option_list import Option

from .base_screen import BaseScreen


class MainScreen(BaseScreen):
    BINDINGS = [
        ("left", "focus_left", "Move Left"),
        ("right", "focus_right", "Move Right"),
    ]

    def compose_body(self) -> ComposeResult:

        with Horizontal():
            yield Label("Welcome to RSS TUI!")
            # Index Column
            with Vertical(id="feeds"):
                yield Static("Feeds")
                yield OptionList(
                    *[Option(f"Feed {i}") for i in range(1, 6)], id="feeds_list"
                )
            # Rows Column
            with Vertical(id="items"):
                yield Static("Items")
                yield OptionList(
                    *[Option(f"Article {i}") for i in range(1, 101)],
                    id="items_list",
                )

            # Preview Column
            with Vertical(id="content"):
                yield Static("Content")
                yield Static("Select an article to read...", id="content_view")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit-app":
            self.app.exit(message="Config not created.")
