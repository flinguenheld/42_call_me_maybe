from src.visual.tmarkdown import TMarkdown


class TBlahBlah(TMarkdown):
    def __init__(self):
        super().__init__(title="Blabla")

    def update_current(self, current: str = ""):
        self.area.update(current)
