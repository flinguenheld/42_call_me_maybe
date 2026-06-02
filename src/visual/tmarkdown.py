from textual.app import ComposeResult
from textual.widgets import Static, Markdown


class TMarkdown(Static):
    def __init__(self, title: str, id: str):
        super().__init__()
        self.area = Markdown(id=id)
        self.border_title = title

    def update_current(self, current: str = ""):
        pass

    def compose(self) -> ComposeResult:
        yield self.area

    def on_mount(self) -> None:
        self.update_current()
