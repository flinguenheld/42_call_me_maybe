from textual.app import App
from dataclasses import dataclass

from src.visual.tprompt import TPrompt
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList
from src.visual.tfunction_list import TFunctionList


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
    widget_function_list: TFunctionList

    # ########################################################################
    # ######################################################### BLAHBLAH #####
    def blah_up(self, who: int, what: str) -> None:
        self.app.call_from_thread(self.widget_blahblah.up, who, what)

    def blah_save_log(self, entry: str) -> None:
        self.widget_blahblah.save_value(entry)

    def blah_clear(self) -> None:
        self.app.call_from_thread(self.widget_blahblah.clear)

    # ########################################################################
    # ########################################################### PROMPT #####
    def prompt_up(self, text: str = "") -> None:
        self.app.call_from_thread(self.widget_prompt.up, text)

    # ########################################################################
    # ###################################################### PROMPT LIST #####
    def prompt_list_up(self, current: str = "") -> None:
        self.app.call_from_thread(self.widget_prompt_list.up, current)

    # ########################################################################
    # #################################################### FUNCTION LIST #####
    def function_list_up(self) -> None:
        self.app.call_from_thread(self.widget_function_list.up)

    # ########################################################################
    # ############################################################# LOGS #####
    def display_logs(self) -> None:
        self.app.call_from_thread(self.widget_blahblah.display_saved_log)
        self.app.call_from_thread(self.widget_prompt.display_saved_log)

    def clear_logs(self) -> None:
        self.widget_blahblah.saved_log.clear()
        self.widget_prompt.saved_log.clear()
