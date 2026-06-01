from src.utils.debug_printer import DebugPrinter
from src.error.error import CallMeError
from dataclasses import dataclass

from src.talker.talker import Talker
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▄░█▀█░█▄█░█▀▀░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀█░█▀▄░█▀█░█░█░█▀▀░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerParameter(Talker):
    function: ModelFunction

    def __post_init__(self) -> None:

        self._prompt = f"""
<|im_start|>system
You are a function parameter extractor.
Given a prompt, a function signature, a description,
extract all arguments from the prompt as JSON.

Rules:
- Do not answer the prompt
- Do not output anything else
- Output ONLY in JSON format
- Do not add space nor new line
- If required, convert the argument into digits (e.g. "forty two" → 42)
- If an argument cannot be found, set it to None
- Add <|endoftext|> at the end of JSON

<example>
prompt: "What is the sum of 100 and 8?"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
arguments:{{"a":100,"b":8}}<|endoftext|>
</example>

<example>
prompt: "Add one to fifteen"
function: "fn_add_numbers(param_a: int, param_b: int)"
description: "Add two numbers together and return their sum."
arguments:{{"param_a":1,"param_b":15}}<|endoftext|>
</example>

<|im_end|>
<|im_start|>user
prompt: "{self.question}"
function: "{self.function.prototype()}"
description: "{self.function.description}"
<|im_end|>
<|im_start|>assistant
<think>

</think>
arguments:
"""
        super().__post_init__()


@CallMeError.catch("Get parameters")
def get_parameters(
    llm: LLMWrapper,
    question: str,
    function: ModelFunction,
    deb: DebugPrinter,
):
    talker_parameter = TalkerParameter(
        llm=llm,
        question=question,
        function=function,
        deb=deb,
    )
    parameters = talker_parameter.talk()

    print(f"parameters -> {parameters}")

    # if argument:
    #     try:
    #         return float(argument)
    #     except ValueError:
    #         raise CallMeError(
    #             prompt=question,
    #             parameter=parameter,
    #             why=f"Impossible to convert '{argument}' in float",
    #         )

    # raise CallMeError(
    #     prompt=question,
    #     parameter=parameter,
    #     why="Parameter research has failed",
    # )
