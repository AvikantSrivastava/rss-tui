from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from feedr.screens.base_screen import BaseScreen
from feedr.services.data import get_feed_data, mark_article_read


def _option_label(title: str, read: bool) -> str:
    """Format an article option label with read/unread indicator."""
    if read:
        return f"[dim]  {title}[/dim]"
    return f"[bold green]●[/bold green] {title}"


class MainScreen(BaseScreen):
    BINDINGS = [
        ("right", "focus_articles", "Articles"),
        ("left", "focus_feeds", "Feeds"),
        ("space", "mark_read", "Mark read"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}

    def compose_body(self) -> ComposeResult:
        with Horizontal():
            # FEEDS COLUMN
            with Vertical(id="feeds"):
                yield Static("Feeds")
                yield OptionList(
                    id="feeds_list",
                    classes="feed_box",
                )

            # ARTICLES COLUMN
            with Vertical(id="items"):
                yield Static("Articles")
                yield OptionList(id="items_list", classes="article_box")

            # CONTENT COLUMN
            with Vertical(id="content"):
                yield Static("Content")
                yield Static(
                    "Select an article...", id="content_view", classes="preview_box"
                )

    def on_mount(self):
        self.feeds = self.query_one("#feeds_list", OptionList)
        self.articles = self.query_one("#items_list", OptionList)
        self.content = self.query_one("#content_view", Static)
        self.load_data()
        self.feeds.focus()

    def on_screen_resume(self):
        """Reload data when returning from another screen (e.g., after refresh)."""
        self.load_data()

    def load_data(self):
        """Load data from database and populate feeds list."""
        self.data = get_feed_data()
        self.feeds.clear_options()
        for feed_name in self.data.keys():
            self.feeds.add_option(Option(feed_name, id=feed_name))

    # → move to articles
    def action_focus_articles(self):
        if self.feeds.has_focus:
            self.articles.focus()

    # ← move back to feeds
    def action_focus_feeds(self):
        if self.articles.has_focus:
            self.feeds.focus()

    # FEED HIGHLIGHTED
    @on(OptionList.OptionHighlighted, "#feeds_list")
    def feed_changed(self, event: OptionList.OptionHighlighted):

        feed_name = event.option.id
        articles = self.data.get(feed_name, {})

        self.articles.clear_options()

        for i, (article_id, article) in enumerate(articles.items()):
            if i >= 100:
                break

            label = _option_label(article["title"], article["read"])
            self.articles.add_option(Option(label, id=article_id))

    # ARTICLE HIGHLIGHTED
    @on(OptionList.OptionHighlighted, "#items_list")
    def article_changed(self, event: OptionList.OptionHighlighted):

        if self.feeds.highlighted is None:
            return
        feed_option = self.feeds.get_option_at_index(self.feeds.highlighted)
        feed_name = feed_option.id

        article_id = event.option.id
        article = self.data[feed_name][article_id]

        self.content.update(
            f"[b]{article['title']}[/b]\n\n{article['description']}"
        )

    def action_mark_read(self):
        """Mark the currently highlighted article as read."""
        if not self.articles.has_focus:
            return
        if self.articles.highlighted is None:
            return
        if self.feeds.highlighted is None:
            return

        feed_option = self.feeds.get_option_at_index(self.feeds.highlighted)
        feed_name = feed_option.id

        article_option = self.articles.get_option_at_index(self.articles.highlighted)
        article_id = article_option.id
        article = self.data[feed_name].get(article_id)

        if article is None or article["read"]:
            return

        # Update DB
        mark_article_read(article["id"])

        # Update local cache
        article["read"] = True

        # Update the option label in-place
        new_label = _option_label(article["title"], True)
        self.articles.replace_option_prompt_at_index(
            self.articles.highlighted, new_label
        )
