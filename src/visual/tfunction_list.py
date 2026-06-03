from typing import List

from src.visual.tmarkdown import TMarkdown
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░░█░░░▀█▀░█▀▀░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░█░░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░░░█░░░░█░░▀▀█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░░▀▀▀░▀▀▀░▀▀▀░░▀░░░
class TFunctionList(TMarkdown):
    def __init__(self, function_list: List[ModelFunction]) -> None:
        super().__init__(title="Functions")
        self.elements = function_list

    def up_list(self) -> None:
        document = "```python\n"
        for function in self.elements:
            document += f"{function.prototype()}\n\n"

        document += "```"
        self.update_document(document)

    def on_mount(self) -> None:
        self.up_list()
