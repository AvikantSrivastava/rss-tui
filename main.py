from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class RSSApp(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def on_mount(self) -> None:
        self.title = "RSS TUI"
        self.sub_title = "A simple RSS reader developed by Avikant"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = RSSApp()
    app.run()
