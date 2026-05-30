from typing import List
from dataclasses import dataclass
from utils.utils import print_debug
from manager.manager import LLMManager


@dataclass()
class LLMManagerAttr(LLMManager):
    def __post_init__(self) -> None:
        self._prompt = """
<|im_start|>system
You are an attribute seeker assistant.
Given the following function:
fn_add_numbers(a: int, b: int)
<|im_end|>
<|im_start|>user
User request: 'What is the sum of 2 and 3?'
<|im_end|>
<|im_start|>system
Find the value of the attribute a
Give only the VALUE OF THE ATTRIBUTE:
<|im_end|>
<|im_start|>assistant
value:
<|im_end|>
"""
        # self.constraint.encode_names(self.llm.encode)
        self._prompt_encoded = self.llm.encode(self._prompt)[0].tolist()
        print_debug(self.debug, f"Prompt: '{self._prompt}'")

    def _index_max_value(self, values: List[float]) -> int:
        """Get the index of the maximum value"""

        print_debug(
            self.debug,
            f"Authorized str:\n'{
                self.llm.decode([t for t in self.constraint.authorised_tokens])
            }'",
        )

        # index = next(iter(self.constraint.authorised_tokens))
        index = 0
        for i in range(1, len(values) - 1):
            if (
                values[i] > values[index]
                # i in self.constraint.authorised_tokens
                # and values[i] > values[index]
            ):
                print(f"here: {i} -> {self.llm.decode([i])} -> {values[i]}")
                index = i

        return index

    def next_token(self) -> None:

        turn = 0
        while True:
            print_debug(self.debug, f"---------------------- turn {turn} ---")
            turn += 1

            # Update the list of authorized tokens
            # self.constraint.next_column()

            logits: List[float] = self.llm.get_logits_from_input_ids(
                self._prompt_encoded
            )

            maxi = self._index_max_value(logits)
            self.constraint.add_current(maxi)
            print_debug(
                self.debug,
                f"token selected: '{maxi}' -> '{self.llm.decode([maxi])}'",
            )

            function_name = self.constraint.get_final_choice()
            if function_name:
                print_debug(self.debug, f"Function found {function_name} ---")
                break

            self._prompt_encoded.append(maxi)
