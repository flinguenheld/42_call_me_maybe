from typing import List

from src.visual.tmarkdown import TMarkdown
from src.models.function_definition import ModelFunction


class TFunctionList(TMarkdown):
    def __init__(self, function_list: List[ModelFunction]):
        super().__init__(title="Functions", id="function_list")
        self.elements = function_list

    def update_current(self, current: str = ""):
        txt = ""
        for function in self.elements:
            if current == function.name:
                txt += f"```python\n{function.prototype()}\n```\n"
            else:
                txt += f"##### {function.prototype()}\n"
        self.area.update(txt)
