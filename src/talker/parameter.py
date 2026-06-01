from itertools import count
from typing import List
from dataclasses import dataclass

from src.talker.talker import Talker
from src.utils.utils import pdebug
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▄░█▀█░█▄█░█▀▀░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀█░█▀▄░█▀█░█░█░█▀▀░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerParameter(Talker):
    function: ModelFunction
    to_find: str

    def __post_init__(self) -> None:
        super().__post_init__()

        self._prompt = f"""
<|im_start|>system
You are a function parameter extractor.
Given a prompt, a function signature, a description, and a parameter to find,
extract the argument of that parameter from the prompt.

Rules:
- Do not answer the prompt
- Do not output anything else
- Output ONLY: argument:X<|endoftext|>
- Do not think, output the argument directly
- If the argument is a number, convert it to digits (e.g. "fifty two" → 52)
- If the argument is a string, return it without quotes

<example>
prompt: "What is the sum of 2 and 5?"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
parameter to find: "a"
argument:2<|endoftext|>
</example>

<example>
prompt: "Add forty two and fifteen"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
parameter to find: "a"
argument:42<|endoftext|>
</example>

<example>
prompt: "Translate 'good morning' to spanish"
function: "fn_translate(text: string, language: string) -> string"
description: "Translate a text to a given language."
parameter to find: "text"
argument:good morning<|endoftext|>
</example>
<|im_end|>

<|im_start|>user
prompt: "{self.question}"
function: "{self.function.prototype()}"
description: "{self.function.description}"
parameter to find: "{self.to_find}"
<|im_end|>
<|im_start|>assistant
<think>

</think>
argument:
"""
        self._prompt_encoded = self.llm.encode(self._prompt)
        pdebug(self.debug, f"Prompt: '{self._prompt}'", colour="yellow")

    def _token_with_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the llm

        token = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[token]:
                token = i
        return token

    def talk(self) -> None:
        for turn in count():
            pdebug(self.debug, f"turn {turn}", title=True)

            logits: List[float] = self.llm.get_logits(self._prompt_encoded)
            maxi = self._token_with_max_value(logits)
            pdebug(self.debug, f"choice: '{maxi}'->'{self.llm.decode(maxi)}'")

            if maxi == self.llm.end or maxi == self.llm.end_of_text:
                break

            self._prompt_encoded.append(maxi)
