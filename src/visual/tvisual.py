from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from src.utils.files import Files
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.talker.talker_manager import TalkerManager

from src.visual.tpaths import TPaths
from src.visual.tprompt import TPrompt
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList
from src.visual.tfunction_list import TFunctionList
from src.visual.visual_printer import VisualPrinter


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
        files: Files,
    ) -> None:
        super().__init__()
        self.llm = llm

        self.files = files
        self.output_list = files.outputs
        self.prompt_list = files.prompts
        self.tprompt_list = TPromptList(files)
        self.function_list = files.functions
        self.tfunction_list = TFunctionList(files)
        self.tpaths = TPaths(files, llm)
        self.tprompt = TPrompt()
        self.tblahblah = TBlahBlah()

        self.visual_printer = VisualPrinter(
            self,
            widget_prompt=self.tprompt,
            widget_blahblah=self.tblahblah,
            widget_prompt_list=self.tprompt_list,
        )

    # ########################################################################
    # ########################################################## CALL ME #####
    @work(exclusive=True, thread=True)
    def call_me_maybe(self) -> None:
        self.output_list.clear()
        manager = TalkerManager(self.llm, self.files, self.visual_printer)

        for prompt in self.prompt_list:
            self.visual_printer.clear_blah()
            manager.manage_one_prompt(prompt=prompt.text)

        # Clear at the end (has to be in the thread)
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
        yield self.tprompt
        yield self.tprompt_list
        yield self.tblahblah
        yield self.tfunction_list
        yield self.tpaths
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Call me maybe"
        self.action_next_theme()
