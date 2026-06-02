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


@CallMeError.catch("Manage prompt")
def manage_prompt(llm: LLMWrapper, question: str) -> ModelOutput:

    output = ModelOutput.model_construct()
    output.prompt = question
    output.parameters = {}

    deb.print(" \nFUNCTION\n ", col="cyan", title=True)
    talker_function = TalkerFunction(
        llm=llm,
        question=question,
        functions=fonction_list,
        deb=deb,
    )

    talker_function.talk()
    if talker_function.found:
        deb.print(" \nPARAMETERS\n ", col="cyan", title=True)
        function = talker_function.found
        output.name = function.name

        talker_parameters = TalkerParameter(
            llm=llm,
            question=question,
            deb=deb,
        )

        print(f"HERE THE QUESTION: '{question}'")
        talker_parameters.get_arguments(function, output, deb)
        print(output)
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    return output


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

            app = TVisual(
                prompt_list=prompts_list,
                function_list=fonction_list,
            )
            app.run()

            # llm = LLMWrapper.create_llm()
            # llm.print_paths(deb)

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
