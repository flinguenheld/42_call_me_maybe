from src.utils.files import Files

from src.models.output import ModelOutput
from src.visual.tmarkdown import TMarkdown
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀▄░█▀█░█▄█░█▀█░▀█▀░░░█░░░▀█▀░█▀▀░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▀░█▀▄░█░█░█░█░█▀▀░░█░░░░█░░░░█░░▀▀█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀░▀░▀▀▀░▀░▀░▀░░░░▀░░░░▀▀▀░▀▀▀░▀▀▀░░▀░░░
class TPromptList(TMarkdown):
    def __init__(
        self,
        files: Files,
    ):
        super().__init__(title="Prompts")
        self.files = files

    def _get_output(self, prompt: str) -> ModelOutput | None:
        for output in self.files.outputs:
            if output.prompt == prompt:
                return output
        return None

    def _get_function(self, name: str) -> ModelFunction | None:
        for function in self.files.functions:
            if function.name == name:
                return function
        return None

    def format_output(self, current: str) -> str:

        text = ""
        output = self._get_output(current)
        if output:
            function = self._get_function(output.name)
            if function:
                text += "```python\n"
                text += f"{function.prototype()}\n"
                text += f"{output.parameters}\n```"

        return text

    def up_current(self, current: str = "") -> None:
        document = ""
        for prompt in self.files.prompts:
            if current == prompt.text:
                document += f"### -> {prompt.text} <-\n"
            else:
                document += f"###### {prompt.text}\n"
                output = self.format_output(prompt.text)
                if output:
                    document += f"{output}\n"
        self.update_document(document)

    def on_mount(self) -> None:
        self.up_current()
