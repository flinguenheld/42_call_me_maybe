from src.visual.tmarkdown import TMarkdown


class TPrompt(TMarkdown):
    def __init__(self):
        super().__init__(title="Current prompt")

    def update_current(self, current: str = ""):
        self.area.update(current)
