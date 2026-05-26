from parser_call_me import parse_call_me
from termcolor import cprint

if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)

    print("hello")
