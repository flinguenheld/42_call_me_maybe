from textual.app import App
from dataclasses import dataclass

from src.visual.tprompt import TPrompt
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList


# ░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░█▀▀░█░█░█▀█░█░░░░░█▀█░█▀▄░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░▀▄▀░░█░░▀▀█░█░█░█▀█░█░░░░░█▀▀░█▀▄░░█░░█░█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░░░▀░░░▀░▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
@dataclass
class VisualPrinter:
    app: App
    widget_prompt: TPrompt
    widget_blahblah: TBlahBlah
    widget_prompt_list: TPromptList

    # ########################################################################
    # ######################################################### BLAHBLAH #####
    def up_blah(self, who: int, what: str) -> None:
        self.app.call_from_thread(self.widget_blahblah.up, who, what)

    def clear_blah(self) -> None:
        self.app.call_from_thread(self.widget_blahblah.clear)

    # ########################################################################
    # ########################################################### PROMPT #####
    def up_prompt(self, text: str = "") -> None:
        self.app.call_from_thread(
            self.widget_prompt.up,
            text,
        )

    # ########################################################################
    # ###################################################### PROMPT LIST #####
    def up_prompt_list(self, current: str = "") -> None:
        self.app.call_from_thread(self.widget_prompt_list.up, current)
