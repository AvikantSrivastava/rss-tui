from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from feedr.dummy_data import DUMMY_FEED
from feedr.screens.base_screen import BaseScreen


class MainScreen(BaseScreen):
    BINDINGS = [
        ("right", "focus_articles", "Articles"),
        ("left", "focus_feeds", "Feeds"),
    ]

    def compose_body(self) -> ComposeResult:
        with Horizontal():
            # FEEDS COLUMN
            with Vertical(id="feeds"):
                yield Static("Feeds")
                yield OptionList(
                    *[Option(feed, id=feed) for feed in DUMMY_FEED.keys()],
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

        self.feeds.focus()

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
        articles = DUMMY_FEED.get(feed_name, {})

        self.articles.clear_options()

        for i, (article_id, article) in enumerate(articles.items()):
            if i >= 100:
                break

            self.articles.add_option(Option(article["title"], id=article_id))

    # ARTICLE HIGHLIGHTED
    @on(OptionList.OptionHighlighted, "#items_list")
    def article_changed(self, event: OptionList.OptionHighlighted):

        feed_option = self.feeds.get_option_at_index(self.feeds.highlighted)
        feed_name = feed_option.id

        article_id = event.option.id
        article = DUMMY_FEED[feed_name][article_id]

        self.content.update(
            f"[b]{article['title']}[/b]\n\n{article['description']}\n\n{article['content']}"
        )
