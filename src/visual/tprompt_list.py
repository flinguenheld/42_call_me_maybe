from typing import List

from src.models.prompt import ModelPrompt
from src.visual.tmarkdown import TMarkdown


class TPromptList(TMarkdown):
    def __init__(self, prompt_list: List[ModelPrompt]):
        super().__init__(title="Prompts")
        self.elements = prompt_list

    def update_current(self, current: str = ""):
        txt = ""
        for prompt in self.elements:
            if current == prompt.text:
                txt += f"##### ->{prompt.text}<-\n"
            else:
                txt += f"###### {prompt.text}\n"
        self.area.update(txt)
