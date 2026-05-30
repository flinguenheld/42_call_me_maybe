from manager.constraint_attribute import Constraint_Attribute
from llm_sdk import Small_LLM_Model
from manager.constraint import Constraint
from manager.manager_attribute import LLMManagerAttr
from typing import List
from models.prompt import parse_prompts
from models.function_definition import parse_functions, FuncDef
from parser_call_me import parse_call_me
from termcolor import cprint
from error.error import CallMeError
from manager.manager_function import LLMManagerFunc
from manager.constraint_function import Constraint_functions


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        # TODO: ADD A LLM WRAPPER TO EASILY CONVERVT TENSOR INTO LIST[INT]
        # TODO: ADD A LLM WRAPPER TO EASILY CONVERVT TENSOR INTO LIST[INT]
        # TODO: ADD A LLM WRAPPER TO EASILY CONVERVT TENSOR INTO LIST[INT]
        try:
            fn_defs: List[FuncDef] = parse_functions(arguments["definitions"])
            prompts = parse_prompts(arguments["input"])

            llm = Small_LLM_Model()

            # llm = LLMManager("Add 3 and 2", Constraint_functions(fn_defs))
            manager_func = LLMManagerFunc(
                llm=llm,
                question="Greet john",
                constraint=Constraint_functions(
                    encode=llm.encode, decode=llm.decode, functions_def=fn_defs
                ),
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

            llm2 = LLMManagerAttr(
                llm=llm,
                question="Greet john",
                constraint=Constraint_Attribute(
                    encode=llm.encode, decode=llm.decode
                ),
                debug=True,
            )

            llm2.next_token()

        except CallMeError as e:
            e.print()
