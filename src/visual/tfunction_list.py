from typing import List

from src.visual.tmarkdown import TMarkdown
from src.models.function_definition import ModelFunction


class TFunctionList(TMarkdown):
    def __init__(self, function_list: List[ModelFunction]):
        super().__init__(title="Functions")
        self.elements = function_list

    def set_txt(self, text: str = ""):
        document = "```python\n"
        for function in self.elements:
            # if current == function.name:
            #     txt += f"```python\n{function.prototype()}\n```\n"
            # else:
            document += f"{function.prototype()}\n"

        document += "```"
        self.update_document(document)
