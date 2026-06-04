from typing import List
from itertools import count
from dataclasses import dataclass, field

from src.talker.talker import Talker
from src.models.function_definition import ModelFunction
from src.talker.function.function_constraint import ConstraintFunction


# ░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▀░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█░█░█░░░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class TalkerFunction(Talker):
    functions: List[ModelFunction]
    found: ModelFunction | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        self.constraint = ConstraintFunction(functions_def=self.functions)
        self.constraint.encode_names(self.llm.encode)
        self.prompt = f"""
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
        self._encode_prompt()

    # ########################################################################
    # ############################################## GET TOKEN MAX VALUE #####
    def _token_with_max_value(self, values: List[float]) -> int:
        """
        Loop in the given logits to find the highest.
        Filter them to the constraint list

        -> Tokens are used as indexes in values by the LLM.
        """

        self.printer.up_blah(3, f"Authorised tokens: {self._format_auth()}")

        token = next(iter(self.constraint.authorised_tokens))
        for i in range(1, len(values) - 1):
            if (
                i in self.constraint.authorised_tokens
                and values[i] > values[token]
            ):
                token = i
        return token

    # ########################################################################
    # ############################################################# TALK #####
    def talk(self) -> None:
        """
        Turn after turn:
          - Get the best token given by the LLM
          - Remove functions which do not contain the token at this column

        Stop when it lefts only one function in the constraint
        """
        for turn in count():
            self.printer.up_blah(2, f"```python\nturn {turn}\n```\n")

            self.constraint.update_authorised_tokens(turn)
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)
            maxi = self._token_with_max_value(logits)
            self.constraint.add_current(maxi)
            self.prompt_encoded.append(maxi)
            self.printer.up_blah(4, self.llm.decode(maxi))

            self.found = self.constraint.get_final_choice()
            if self.found:
                self.printer.up_blah(3, f"Function found: {self.found.name}")
                break

    # ########################################################################
    # ##################################################### PRINT HELPER #####
    def _format_auth(self) -> str:
        text = ""
        for token in self.constraint.authorised_tokens:
            text += f"'{self.llm.decode(token)}' "
        return text
