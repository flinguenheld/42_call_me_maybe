from function_definintion.function_definition import (
    # FunctionDefinition,
    parse_functions,
)
from parser_call_me import parse_call_me
from termcolor import cprint
from error.error import CallMeError

if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            model = parse_functions(arguments["definitions"])
            print(model)
        except CallMeError as e:
            e.print()

    print("hello")
