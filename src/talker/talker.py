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
    _prompt: str = field(init=False)
    _prompt_encoded: List[int] = field(init=False, default_factory=list)
    # _token_numbers: List[int] = field(default_factory=list)

    def __post_init__(self):
        self._prompt_encoded = self.llm.encode(self._prompt)
        self.deb.print(f"Prompt: '{self._prompt}'", col="yellow")

    def _token_with_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the llm

        token = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[token]:
                token = i
        return token

    def talk(self) -> str | None:
        current = ""
        for turn in count():
            self.deb.print(f"turn {turn}", title=True)

            logits: List[float] = self.llm.get_logits(self._prompt_encoded)
            token = self._token_with_max_value(logits)

            if token == self.llm.think_start or token == self.llm.think_end:
                continue
            if token == self.llm.end or token == self.llm.end_of_text:
                return current

            current += self.llm.decode(token)
            self._prompt_encoded.append(token)
            self.deb.print(f"'{self.llm.decode(token)}' -> '{current}'")

        return None
