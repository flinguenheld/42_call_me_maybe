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
    """
    Update markdown widgets with the call_from_thread method.
    Have to be used in a thread.
    """

    app: App
    widget_prompt: TPrompt
    widget_blahblah: TBlahBlah
    widget_prompt_list: TPromptList

    # ########################################################################
    # ######################################################### BLAHBLAH #####
    def blah_up(self, who: int, what: str) -> None:
        self.app.call_from_thread(self.widget_blahblah.up, who, what)

    def blah_save_log(self, entry: str) -> None:
        self.widget_blahblah.save_value(entry)

    def blah_display_log(self) -> None:
        self.app.call_from_thread(self.widget_blahblah.display_saved_log)

    def blah_clear(self, include_logs: bool = True) -> None:
        self.app.call_from_thread(self.widget_blahblah.clear, include_logs)

    # ########################################################################
    # ########################################################### PROMPT #####
    def prompt_up(self, text: str = "") -> None:
        self.app.call_from_thread(
            self.widget_prompt.up,
            text,
        )

    # ########################################################################
    # ###################################################### PROMPT LIST #####
    def prompt_list_up(self, current: str = "") -> None:
        self.app.call_from_thread(self.widget_prompt_list.up, current)
