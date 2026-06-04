from src.utils.files import Files
from src.visual.tmarkdown import TMarkdown


class TFunctionList(TMarkdown):
    def __init__(self, files: Files) -> None:
        super().__init__(title="Functions")
        self.files = files

    def up_document(self) -> None:
        document = "```python\n"
        for function in self.files.functions:
            document += f"{function.prototype()}\n"
        document += "```\n"

        self.update_document(document)

    def on_mount(self) -> None:
        self.up_document()
