from typing import List
from src.visual.tmarkdown import TMarkdown


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█▀▄░█▀█░█▄█░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀▀░█▀▄░█░█░█░█░█▀▀░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░░░▀░▀░▀▀▀░▀░▀░▀░░░░▀░░░
class TPrompt(TMarkdown):
    def __init__(self) -> None:
        super().__init__(title="Current prompt")
        self.saved_log: List[str] = list()

    # ########################################################################
    # ############################################################### UP #####
    def up(self, txt: str = "") -> None:
        self.saved_log.append(f"```text\n{txt}\n```")
        self.update_document(self.saved_log[-1])

    # ########################################################################
    # ######################################################## SAVED LOG #####
    def display_saved_log(self) -> None:
        self.update_document("\n--\n".join(self.saved_log))
