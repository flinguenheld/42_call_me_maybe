from typing import List
from dataclasses import dataclass

from src.talker.talker import Talker
from src.utils.utils import print_debug


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░▀█▀░▀█▀░█▀▄░▀█▀░█▀▄░█░█░▀█▀░█▀▀░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀█░░█░░░█░░█▀▄░░█░░█▀▄░█░█░░█░░█▀▀░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░░▀░░░▀░░▀░▀░▀▀▀░▀▀░░▀▀▀░░▀░░▀▀▀░░
@dataclass()
class TalkerAttribute(Talker):
    def __post_init__(self) -> None:
        super().__post_init__()

        self._prompt = """
<|im_start|>system
You are a function argument extractor.
Given a prompt, a function signature, a description, and an argument to find,
extract the value of that argument from the prompt.

Rules:
- Do not answer the prompt
- Do not output anything else
- Output ONLY: value:X<|endoftext|>
- Do not think, output the value directly
- If the value is a number, convert it to digits (e.g. "fifty two" → 52)

<example>
prompt: "What is the sum of 2 and 5?"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
argument to find: "a"
value:2<|endoftext|>
</example>

<example>
prompt: "Add forty two and fifteen"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
argument to find: "a"
value:42<|endoftext|>
</example>
<|im_end|>
<|im_start|>user
prompt: "What is the sum of fifty and thirty five?"
function: "fn_add_numbers(a: int, b: int)"
description: "Add two numbers together and return their sum."
argument to find: "a"
<|im_end|>
<|im_start|>assistant
<think>

</think>
value:
"""
        # self.constraint.encode_names(self.llm.encode)
        self._prompt_encoded = self.llm.encode(self._prompt)
        print_debug(self.debug, f"Prompt: '{self._prompt}'")

    def _index_max_value(self, values: List[float]) -> int:
        """Get the index of the maximum value"""

        index = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[index]:
                index = i

        return index

    def next_token(self) -> None:

        print_debug(self.debug, f"end of text token: {self.llm.end_of_text}")
        print_debug(self.debug, f"151645: {self.llm.decode(151645)}")

        turn = 0
        while True:
            print_debug(self.debug, f"---------------------- turn {turn} ---")
            turn += 1

            logits: List[float] = self.llm.get_logits(self._prompt_encoded)

            maxi = self._index_max_value(logits)
            print_debug(
                self.debug,
                f"token selected: '{maxi}' -> '{self.llm.decode([maxi])}'",
            )

            if maxi == self.llm.end or maxi == self.llm.end_of_text:
                break

            self._prompt_encoded.append(maxi)
