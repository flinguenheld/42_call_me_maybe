from typing import List
from textual.app import App
from dataclasses import dataclass

from src.visual.tprompt import TPrompt
from src.models.prompt import ModelPrompt
from src.visual.tblahblah import TBlahBlah
from src.visual.tprompt_list import TPromptList


@dataclass
class VisualPrinter:
    app: App
    widget_blah: TBlahBlah
    widget_prompt: TPrompt

    prompt_list: List[ModelPrompt]
    widget_prompt_list: TPromptList

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

    def up_prompt_list(self, current: str = "") -> None:
        self.app.call_from_thread(self.widget_prompt_list.up_current, current)
