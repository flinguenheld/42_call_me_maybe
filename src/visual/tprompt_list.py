from typing import List

from src.models.prompt import ModelPrompt
from src.visual.tmarkdown import TMarkdown


class TPromptList(TMarkdown):
    def __init__(self, prompt_list: List[ModelPrompt]):
        super().__init__(title="Prompts")
        self.elements = prompt_list

    def set_txt(self, current: str = ""):
        document = ""
        for prompt in self.elements:
            if current == prompt.text:
                document += f"##### ->{prompt.text}<-\n"
            else:
                document += f"###### {prompt.text}\n"
        self.update_document(document)
