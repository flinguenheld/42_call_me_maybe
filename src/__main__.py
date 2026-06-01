from typing import List
from termcolor import cprint
from src.error.error import CallMeError
from src.models.prompt import parse_prompts
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.utils.utils import pdebug
from src.utils.parser_call_me import parse_call_me
from src.talker.function import TalkerFunction
from src.talker.parameter import TalkerParameter
from src.models.function_definition import parse_functions, ModelFunction


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            debug = True
            fn_defs: List[ModelFunction] = parse_functions(
                arguments["definitions"]
            )
            prompts = parse_prompts(arguments["input"])

            llm = LLMWrapper()
            prompt_test = "What is the sum of 265 and 345?"
            # prompt_test = "Reverse the string 'hello'"

            pdebug(debug, " \nFUNCTION\n ", colour="cyan", title=True)
            talker_function = TalkerFunction(
                llm=llm,
                # question="Greet john",
                question=prompt_test,
                functions=fn_defs,
                debug=debug,
            )

            talker_function.talk()
            # for _ in range(5):
            if talker_function.found:
                pdebug(debug, " \nPARAMETERS\n ", colour="cyan", title=True)
                function = talker_function.found
                for key, val in function.parameters.items():
                    pdebug(debug, f"Search parameter {key} {val}", title=True)

                    talker_parameter = TalkerParameter(
                        llm=llm,
                        question=prompt_test,
                        to_find="s",
                        function=talker_function.found,
                        debug=debug,
                    )

                talker_parameter.talk()

        except CallMeError as e:
            e.print()
