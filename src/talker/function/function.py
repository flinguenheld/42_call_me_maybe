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
        super().__post_init__()

    def _token_with_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the llm

        self.deb.print(f"Authorized tokens: {self._debug_format_auth()}")
        token = next(iter(self.constraint.authorised_tokens))
        for i in range(1, len(values) - 1):
            if (
                i in self.constraint.authorised_tokens
                and values[i] > values[token]
            ):
                token = i
        return token

    def talk(self) -> None:
        for turn in count():
            self.deb.print(f"turn {turn}", title=True)

            self.constraint.update_authorised_tokens(turn)
            logits: List[float] = self.llm.get_logits(self._prompt_encoded)
            maxi = self._token_with_max_value(logits)
            self.constraint.add_current(maxi)
            self._prompt_encoded.append(maxi)
            self.deb.print(f"choice: '{maxi}'->'{self.llm.decode(maxi)}'")

            self.found = self.constraint.get_final_choice()
            if self.found:
                self.deb.print(f"Function found: '{self.found.name}'")
                break

    def _debug_format_auth(self):
        text = ""
        for token in self.constraint.authorised_tokens:
            text += f"'{self.llm.decode(token)}' "
        return text
