from termcolor import cprint

# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░▀█▀░▀█▀░█░░░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░░█░░░█░░█░░░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░░▀░░▀▀▀░▀▀▀░▀▀▀░░


def print_debug(debug: bool, txt: str, colour: str = "blue") -> None:
    if debug:
        for line in txt.splitlines():
            cprint("    -> ", "grey", end="")
            cprint(f"{line}", colour)
