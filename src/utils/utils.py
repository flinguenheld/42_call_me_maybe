from termcolor import cprint

# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░█░░█░░░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░░


def pdebug(
    debug: bool, txt: str, colour: str = "blue", title: bool = False
) -> None:
    if debug:
        for line in txt.splitlines():
            cprint("    -> ", "grey", end="")
            if title:
                cprint("##### ", colour, end="")
            cprint(f"{line}", colour, end="")

            to_fill = 130 - len(line)
            if to_fill > 0:
                if title:
                    cprint(" ", end="")
                    cprint("#" * (to_fill - 7), colour, end="")
                else:
                    cprint(" " * to_fill, end="")
            cprint(" <-", "grey")
