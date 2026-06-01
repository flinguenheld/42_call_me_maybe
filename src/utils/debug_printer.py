from termcolor import cprint
from dataclasses import dataclass


# ░░░░░░░░░░░░░░░░░░░░░░░░░█▀▄░█▀▀░█▀▄░█░█░█▀▀░░░█▀█░█▀▄░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█▀▀░█▀▄░█░█░█░█░░░█▀▀░█▀▄░░█░░█░█░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░▀▀░░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░░
@dataclass
class DebugPrinter:
    active: bool

    def print(self, txt: str, col: str = "blue", title: bool = False) -> None:
        if self.active:
            for line in txt.splitlines():
                cprint("    -> ", "grey", end="")
                if title:
                    cprint("##### ", col, end="")
                cprint(f"{line}", col, end="")

                to_fill = 130 - len(line)
                if to_fill > 0:
                    if title:
                        cprint(" ", end="")
                        cprint("#" * (to_fill - 7), col, end="")
                    else:
                        cprint(" " * to_fill, end="")
                cprint(" <-", "grey")
