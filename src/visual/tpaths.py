from src.utils.files import Files
from src.llm_wrapper.llm_wrapper import LLMWrapper

from src.visual.tmarkdown import TMarkdown


class TPaths(TMarkdown):
    def __init__(self, files: Files, llm: LLMWrapper) -> None:
        super().__init__(title="Paths")
        self.files = files
        self.llm = llm

    def up_document(self) -> None:
        document = f"""> prompts:   {self.files.path_prompts}  
                       > functions: {self.files.path_functions}  
                       > output:    {self.files.path_output}  
                    """
        document += f"\n{self.llm.paths()}"
        self.update_document(document)

    def on_mount(self) -> None:
        self.up_document()
