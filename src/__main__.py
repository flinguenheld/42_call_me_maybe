from src.visual.visual_printer import VisualPrinter
from src.talker.parameter.parameter import TalkerParameter
from typing import List
from termcolor import cprint

from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.models.prompt import parse_prompts
from src.utils.debug_printer import DebugPrinter
from src.utils.parser_call_me import parse_call_me
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.talker.function.function import TalkerFunction
from src.models.function_definition import parse_functions, ModelFunction

from src.visual.tvisual import TVisual


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            deb = DebugPrinter(active=True)
            # deb = DebugPrinter(active=False)
            fonction_list: List[ModelFunction] = parse_functions(
                arguments["definitions"]
            )
            prompts_list = parse_prompts(arguments["input"])

            llm = LLMWrapper.create_llm()
            llm.print_paths(deb)

            app = TVisual(
                llm,
                prompt_list=prompts_list,
                function_list=fonction_list,
            )
            printer: VisualPrinter = app.get_visual_printer()

            app.run()

            # printer.up_blahblah("MY ASS")

            # output = manage_prompt(
            #     # llm,
            #     # "What is the sum of 265 and twenty two?",
            #     # llm,
            #     # "Reverse the string 'world'",
            #     # llm,
            #     # 'Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS',
            #     llm,
            #     "Greet shrek",
            # )
            # print(f"output built: {output}")
            # print(f"PROMPTS  {prompts}")

            # for prompt in prompts:
            #     # print(f"PROMPT SA MERE {prompt}")
            #     output = manage_prompt(llm, prompt.text)
            #     # print(f"output built: {output}")

        except CallMeError as e:
            e.print()
