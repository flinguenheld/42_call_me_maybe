from textual.app import ComposeResult
from textual.widgets import Static, Markdown


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░█▀▄░█░█░█▀▄░█▀█░█░█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░█▀▄░█▀▄░█░█░█░█░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░
class TMarkdown(Static):
    def __init__(self, title: str, classes: str = "") -> None:
        super().__init__(classes=classes)
        self.area = Markdown(classes=classes)
        self.border_title = title

    def update_document(self, document: str = "") -> None:
        self.area.update(document)

    def compose(self) -> ComposeResult:
        yield self.area
