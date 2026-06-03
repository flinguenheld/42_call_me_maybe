from textual.message_pump import MessagePump
from textual.app import App
from typing import List
from dataclasses import dataclass

from src.visual.tprompt import TPrompt
from src.models.prompt import ModelPrompt
from src.models.output import ModelOutput
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList
from src.visual.tfunction_list import TFunctionList
from src.models.function_definition import ModelFunction


@dataclass
class VisualPrinter:
    app: App
    widget_blah: TBlahBlah
    widget_prompt: TPrompt

    prompt_list: List[ModelPrompt]
    widget_prompt_list: TPromptList

    function_list: List[ModelFunction]
    widget_function_list: TFunctionList

    def up_blah(self, who: int, what: str) -> None:
        self.app.call_from_thread(self.widget_blah.set_txt, who, what)

    def clear_blah(self) -> None:
        self.app.call_from_thread(self.widget_blah.clear)

    def up_prompt(self, title: str = "", text: str = "") -> None:
        self.app.call_from_thread(
            self.widget_prompt.set_txt,
            title,
            text,
        )

    def up_prompt_list(self, output: List[ModelOutput]) -> None:
        pass
        # self.widget_prompt.update_current(text)
        # self.up_blahblah()

    def up_function_list(self, output: List[ModelFunction]) -> None:
        pass
        # self.widget_prompt.update_current(text)
        # self.up_blahblah()
