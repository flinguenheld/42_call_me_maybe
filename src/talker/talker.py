from itertools import count
from typing import List
from dataclasses import dataclass, field

from src.utils.debug_printer import DebugPrinter
from src.llm_wrapper.llm_wrapper import LLMWrapper


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░
@dataclass
class Talker:
    question: str
    llm: LLMWrapper
    deb: DebugPrinter
    prompt: str = field(init=False)
    _prompt_encoded: List[int] = field(init=False, default_factory=list)

    def _encode_prompt(self):
        self._prompt_encoded = self.llm.encode(self.prompt)
        self.deb.print(f"Prompt: '{self.prompt}'", col="yellow")

    def _get_token_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the LLM
        token = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[token]:
                token = i
        return token
