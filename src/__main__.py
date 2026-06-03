from typing import List
from termcolor import cprint

from src.visual.tvisual import TVisual
from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.utils.debug_printer import DebugPrinter
from src.utils.parser_call_me import parse_call_me
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.models.prompt import parse_prompts, ModelPrompt
from src.models.function_definition import parse_functions, ModelFunction


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            deb = DebugPrinter(active=True)

            fonction_list: List[ModelFunction] = parse_functions(
                arguments["definitions"]
            )
            prompts_list: List[ModelPrompt] = parse_prompts(arguments["input"])
            output_list: List[ModelOutput] = list()

            llm = LLMWrapper.create_llm()
            llm.print_paths(deb)

            app = TVisual(
                llm,
                prompt_list=prompts_list,
                function_list=fonction_list,
                output_list=output_list,
            )
            app.run()

        except CallMeError as e:
            e.print()
