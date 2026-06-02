from src.visual.tfunction_list import TFunctionList
from src.models.function_definition import ModelFunction
from src.models.prompt import ModelPrompt
from typing import List
from textual.widgets import Header
from textual.app import App, ComposeResult

from src.visual.tprompt_list import TPromptList


class TVisual(App):
    CSS_PATH = [
        "styles/main.tcss",
    ]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        prompt_list: List[ModelPrompt],
        function_list: List[ModelFunction],
    ) -> None:
        super().__init__()
        self.tprompt_list = TPromptList(prompt_list)
        self.tfunction_list = TFunctionList(function_list)

    # ########################################################################
    # ########################################################### THEMES #####
    def action_next_theme(self) -> None:
        match self.theme[-5:]:
            case "uvbox":
                self.theme = "catppuccin-latte"
            case "latte":
                self.theme = "catppuccin-macchiato"
            case "hiato":
                self.theme = "catppuccin-mocha"
            case "mocha":
                self.theme = "catppuccin-frappe"
            case _:
                self.theme = "gruvbox"

    # ########################################################################
    # ################################################### COMPOSE / MOUNT ####
    def compose(self) -> ComposeResult:
        yield Header()
        yield self.tprompt_list
        yield self.tfunction_list

    def on_mount(self) -> None:
        self.title = "Call me maybe"
        self.action_next_theme()
