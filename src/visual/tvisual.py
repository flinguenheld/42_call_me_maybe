from typing import List
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.containers import ScrollableContainer

from src.visual.tprompt import TPrompt
from src.models.prompt import ModelPrompt
from src.models.output import ModelOutput
from src.visual.tblahblah import TBlahBlah
from src.manager.manager import manage_prompt
from src.visual.tprompt_list import TPromptList
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.visual.visual_printer import VisualPrinter
from src.visual.tfunction_list import TFunctionList
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
class TVisual(App):
    CSS_PATH = [
        "styles/main.tcss",
    ]
    BINDINGS = [
        ("t", "next_theme", "Next theme"),
        ("r", "call_me", "Run"),
        ("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        llm: LLMWrapper,
        prompt_list: List[ModelPrompt],
        function_list: List[ModelFunction],
        output_list: List[ModelOutput],
    ) -> None:
        super().__init__()
        self.llm = llm
        self.output_list = output_list

        self.prompt_list = prompt_list
        self.tprompt_list = TPromptList(
            prompt_list, output_list, function_list
        )
        self.function_list = function_list
        self.tfunction_list = TFunctionList(function_list)
        self.tprompt = TPrompt()
        self.tblahblah = TBlahBlah()

        self.visual_printer = VisualPrinter(
            self,
            widget_blah=self.tblahblah,
            widget_prompt=self.tprompt,
            prompt_list=prompt_list,
            widget_prompt_list=self.tprompt_list,
        )

    @work(exclusive=True, thread=True)
    def call_me_maybe(self) -> None:
        self.output_list.clear()

        for prompt in self.prompt_list:
            self.visual_printer.clear_blah()

            manage_prompt(
                self.llm,
                prompt.text,
                self.function_list,
                self.output_list,
                self.visual_printer,
            )

        self.visual_printer.up_prompt()
        self.visual_printer.clear_blah()
        self.visual_printer.up_prompt_list()

    def action_call_me(self) -> None:
        self.call_me_maybe()

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
        with ScrollableContainer(classes="box"):
            yield self.tprompt
        with ScrollableContainer(classes="box"):
            yield self.tprompt_list
        with ScrollableContainer(classes="box"):
            yield self.tblahblah
        with ScrollableContainer(classes="box"):
            yield self.tfunction_list
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Call me maybe"
        self.action_next_theme()
