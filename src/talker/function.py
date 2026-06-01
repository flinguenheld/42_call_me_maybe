from itertools import count
from typing import List
from dataclasses import dataclass, field

from src.talker.talker import Talker
from src.utils.utils import pdebug
from src.models.function_definition import ModelFunction
from src.talker.constraint_function import ConstraintFunction


# ░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▀░█░█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█░█░█░░░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class TalkerFunction(Talker):
    functions: List[ModelFunction]
    found: ModelFunction | None = field(init=False, default=None)

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
        pdebug(self.debug, f"Prompt: '{self._prompt}'", colour="yellow")

    def _token_with_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the llm

        pdebug(self.debug, f"Authorized tokens: {self._debug_format_auth()}")
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
            pdebug(self.debug, f"turn {turn}", title=True)

            self.constraint.update_authorised_tokens(turn)
            logits: List[float] = self.llm.get_logits(self._prompt_encoded)
            maxi = self._token_with_max_value(logits)
            self.constraint.add_current(maxi)
            pdebug(self.debug, f"choice: '{maxi}'->'{self.llm.decode(maxi)}'")

            self.found = self.constraint.get_final_choice()
            if self.found:
                pdebug(self.debug, f"Function found: '{self.found.name}'")
                break

            self._prompt_encoded.append(maxi)

    def _debug_format_auth(self):
        text = ""
        for token in self.constraint.authorised_tokens:
            text += f"'{self.llm.decode(token)}' "
        return text
