from textual.app import ComposeResult
from textual.widgets import Static, Markdown
from textual.containers import ScrollableContainer


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀█░█▀▄░█░█░█▀▄░█▀█░█░█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀█░█▀▄░█▀▄░█░█░█░█░█▄█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░
class TMarkdown(Static):
    def __init__(self, title: str) -> None:
        super().__init__(classes="box")
        self.area = Markdown()
        self.border_title = title

    def update_document(self, document: str = "") -> None:
        self.area.update(document)

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            yield self.area
