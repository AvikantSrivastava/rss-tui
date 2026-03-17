from feedctl.screens.base_screen import BaseScreen
from feedctl.utils import create_config_file
from textual.app import ComposeResult
from textual.containers import Center
from textual.widgets import Label, OptionList
from textual.widgets.option_list import Option


class SetupScreen(BaseScreen):
    def compose_body(self) -> ComposeResult:
        with Center():
            yield Label("Do you want to use the default config?")
            yield OptionList(
                Option("Yes", id="yes"),
                Option("No", id="no"),
            )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "yes":
            create_config_file()
            self.app.switch_screen("main")

        elif event.option.id == "no":
            self.app.exit()
