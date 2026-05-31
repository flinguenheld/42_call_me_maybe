from typing import List
from termcolor import cprint
from src.error.error import CallMeError
from src.models.prompt import parse_prompts
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.utils.parser_call_me import parse_call_me
from src.talker.function import TalkerFunction
from src.talker.attribute import TalkerAttribute
from src.models.function_definition import parse_functions, ModelFunction


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            fn_defs: List[ModelFunction] = parse_functions(
                arguments["definitions"]
            )
            prompts = parse_prompts(arguments["input"])

            llm = LLMWrapper()

            # llm = LLMManager("Add 3 and 2", Constraint_functions(fn_defs))
            manager_func = TalkerFunction(
                llm=llm,
                question="Greet john",
                functions=fn_defs,
                debug=True,
            )
            # llm = LLMManager(
            #     "What is the sum of 265 and 345?", Constraint(fn_defs)
            # )
            # llm = LLMManager(
            #     'Replace all numbers in "Hello 34 I\'m 233 years old"
            # with NUMBERS',
            #     Constraint_functions(fn_defs),
            # )
            # llm = LLMManager(
            #     "Substitute the word 'cat' with 'dog' in 'The
            # cat sat on the mat with another cat'",
            #     Constraint_functions(fn_defs),
            # )
            # llm = LLMManager(
            #     "It's late, does Novanns have to go to bed ?",
            #     Constraint_functions(fn_defs),
            # )

            # llm.next_token()
            # for _ in range(5):
            manager_func.next_token()
            print("#########################################################")
            print("#########################################################")
            print("#########################################################")

            llm2 = TalkerAttribute(
                llm=llm,
                question="Greet john",
                debug=True,
            )

            llm2.next_token()

        except CallMeError as e:
            e.print()
