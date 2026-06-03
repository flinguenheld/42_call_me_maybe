from textual.reactive import reactive
from typing import Dict, List

from src.visual.tmarkdown import TMarkdown


class TBlahBlah(TMarkdown):
    def __init__(self):
        super().__init__(title="Blabla")
        self.lines: Dict[int, str] = dict()

    def clear(self):
        self.lines.clear()

    def set_txt(self, who: int, what: str):
        self.lines[who] = what

        document = ""
        for i in range(0, max(self.lines.keys()) + 1):
            if i in self.lines:
                document += f"{self.lines[i]}\n"

        self.update_document(document)
