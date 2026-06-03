from src.visual.tmarkdown import TMarkdown


class TPrompt(TMarkdown):
    def __init__(self):
        super().__init__(title="Current prompt")

    def set_txt(self, txt: str = "", title: str = ""):
        document = f"### {title}\n"
        document += txt

        self.update_document(document)
