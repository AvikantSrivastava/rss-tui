from feedctl.db.session import cleanup_database, get_db_size_bytes
from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static

CLEANUP_DAYS = 30


def _human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024


class CleanupScreen(ModalScreen):
    """Confirm before deleting old / orphaned articles to reclaim disk space."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        size = _human_size(get_db_size_bytes())
        with Center():
            with Vertical(id="cleanup_dialog"):
                yield Static("[b]Clean up database[/b]")
                yield Static(f"Current size on disk: {size}")
                yield Static(
                    f"This will delete articles older than {CLEANUP_DAYS} days "
                    "and all articles from feeds no longer in your config. "
                    "Feeds and their read/unread state are kept. This cannot be undone."
                )
                with Horizontal(id="cleanup_buttons"):
                    yield Button("Clean up", variant="error", id="confirm")
                    yield Button("Cancel", variant="primary", id="cancel")

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        self.dismiss()

    @on(Button.Pressed, "#confirm")
    def _confirm(self) -> None:
        self.query_one("#cleanup_buttons").disabled = True
        self.run_worker(self._run_cleanup, thread=True)

    def _run_cleanup(self) -> None:
        before = get_db_size_bytes()
        deleted = cleanup_database(CLEANUP_DAYS)
        reclaimed = _human_size(max(before - get_db_size_bytes(), 0))
        self.app.call_from_thread(
            self.app.notify,
            f"Removed {deleted} articles, reclaimed {reclaimed}.",
            title="Cleanup complete",
        )
        self.app.call_from_thread(self.dismiss)
