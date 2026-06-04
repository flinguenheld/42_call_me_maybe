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

    # ########################################################################
    # ############################################################### UP #####
    def up(self, current: str = "") -> None:
        document = "```python\n"
        for prompt in self.files.prompts:
            if current == prompt.text:
                document += f'""" -> {prompt.text} <- """\n\n'
            else:
                output = self.format(prompt.text)
                if output:
                    document += f"{output}\n\n"
                else:
                    document += f"# {prompt.text}\n\n"

        document += "\n```"
        self.update_document(document)

    # ########################################################################
    # ################################################## FORMAT DOCUMENT #####
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

    def format(self, current: str) -> str:

        text = ""
        output = self._get_output(current)
        if output:
            function = self._get_function(output.name)
            if function:
                text += f"# {current}\n"
                text += f"    {function.prototype()}\n"
                text += f"    {output.parameters}\n"

        return text

    # ########################################################################
    # ############################################################ MOUNT #####
    def on_mount(self) -> None:
        self.up()
