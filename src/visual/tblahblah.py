from typing import Dict, List

from src.visual.tmarkdown import TMarkdown


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀▄░█░░░█▀█░█░█░█▀▄░█░░░█▀█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▄░█░░░█▀█░█▀█░█▀▄░█░░░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀▀░░▀▀▀░▀░▀░▀░▀░▀▀░░▀▀▀░▀░▀░▀░▀░░
class TBlahBlah(TMarkdown):
    def __init__(self) -> None:
        super().__init__(title="Blabla")
        self.lines: Dict[int, str] = dict()
        self.saved_log: List[str] = list()

    # ########################################################################
    # ############################################################### UP #####
    def up(self, who: int, what: str) -> None:
        self.lines[who] = what

        document = ""
        for i in range(0, max(self.lines.keys()) + 1):
            if i in self.lines:
                document += f"{self.lines[i]}\n"

        self.update_document(document)

    # ########################################################################
    # ######################################################## SAVED LOG #####
    def save_value(self, to_save: str) -> None:
        self.saved_log.append(to_save)

    def display_saved_log(self) -> None:
        document = "```text\n"
        for entry in self.saved_log:
            document += f"{entry}<--\n"

        self.update_document(document + "\n```")

    # ########################################################################
    # ############################################################ CLEAR #####
    def clear(self, include_logs: bool = True) -> None:
        self.lines.clear()
        if include_logs:
            self.saved_log.clear()
