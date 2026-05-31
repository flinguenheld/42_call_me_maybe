from typing import List
from dataclasses import dataclass

from src.talker.talker import Talker
from src.utils.utils import print_debug
from src.models.function_definition import ModelFunction
from src.talker.constraint_function import ConstraintFunction


# ░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▀░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█░█░█░░░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class TalkerFunction(Talker):
    functions: List[ModelFunction]

    def __post_init__(self) -> None:
        super().__post_init__()
        self.constraint = ConstraintFunction(functions_def=self.functions)

        self.constraint.encode_names(self.llm.encode)
        self._prompt = f"""
<|im_start|>system
You are a function calling assistant.
Given the following available functions:
{self.constraint}
<|im_end|>
<|im_start|>user
User request: "{self.question}"
<|im_end|>
<|im_start|>system
Find the correct function.
Give only the FUNCTION NAME:
<|im_end|>
<|im_start|>assistant
function:
"""
        self._prompt_encoded = self.llm.encode(self._prompt)
        print_debug(self.debug, f"Prompt: '{self._prompt}'")

    def _index_max_value(self, values: List[float]) -> int:
        """Get the index of the maximum value"""

        print_debug(
            self.debug,
            f"Authorized str:\n'{
                self.llm.decode([t for t in self.constraint.authorised_tokens])
            }'",
        )

        index = next(iter(self.constraint.authorised_tokens))
        for i in range(1, len(values) - 1):
            if (
                i in self.constraint.authorised_tokens
                and values[i] > values[index]
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
            self.constraint.next_column()

            logits: List[float] = self.llm.get_logits(self._prompt_encoded)

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
