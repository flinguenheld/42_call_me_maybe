from termcolor import cprint

from src.utils.files import Files
from src.visual.tvisual import TVisual
from src.error.error import CallMeError
from src.utils.debug_printer import DebugPrinter
from src.utils.parser_call_me import parse_call_me
from src.llm_wrapper.llm_wrapper import LLMWrapper


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            deb = DebugPrinter(active=True)
            files = Files(
                path_prompts=arguments["input"],
                path_functions=arguments["definitions"],
                path_output=arguments["output"],
            )

            llm = LLMWrapper.create_llm()
            llm.print_paths(deb)

            app = TVisual(llm, files)
            app.run()

        except CallMeError as e:
            e.print()
