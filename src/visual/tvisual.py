from src.manager.manager import manage_prompt
from textual import work
from src.talker.parameter.parameter import TalkerParameter
from src.talker.function.function import TalkerFunction
from src.models.output import ModelOutput
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.error.error import CallMeError
from src.visual.visual_printer import VisualPrinter
from typing import List
from textual.widgets import Header, Footer
from textual.app import App, ComposeResult

from src.visual.tprompt import TPrompt
from src.models.prompt import ModelPrompt
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList
from src.visual.tfunction_list import TFunctionList
from src.models.function_definition import ModelFunction


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
    ) -> None:
        super().__init__()
        self.llm = llm
        self.prompt_list = prompt_list
        self.tprompt_list = TPromptList(prompt_list)
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
            function_list=function_list,
            widget_function_list=self.tfunction_list,
        )

    @work(exclusive=True, thread=True)
    def call_me_maybe(self):
        for prompt in self.prompt_list:
            self.visual_printer.clear_blah()

            output = manage_prompt(
                self.llm, prompt.text, self.function_list, self.visual_printer
            )
            # print(f"output built: {output}")

    def action_call_me(self):
        # self.visual_printer.up_blahblah("HELLO WORLD")
        self.call_me_maybe()

    # ########################################################################
    # ################################################### VISUAL PRINTER #####
    # TODO: USEFUL ??????????????????????
    # TODO: USEFUL ??????????????????????
    # TODO: USEFUL ??????????????????????
    # TODO: USEFUL ??????????????????????
    def get_visual_printer(self):
        return self.visual_printer

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
        yield self.tprompt
        yield self.tprompt_list
        yield self.tblahblah
        yield self.tfunction_list
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Call me maybe"
        self.action_next_theme()

        self.tprompt.set_txt("hello")
