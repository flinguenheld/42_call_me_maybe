from typing import List
from dataclasses import dataclass, field

from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.visual.visual_printer import VisualPrinter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░
@dataclass
class Talker:
    question: str
    llm: LLMWrapper
    printer: VisualPrinter
    prompt: str = field(init=False)
    _prompt_encoded: List[int] = field(init=False, default_factory=list)

    def _encode_prompt(self) -> None:
        self._prompt_encoded = self.llm.encode(self.prompt)
        self.printer.up_prompt("my title", self.prompt)

    def _get_token_max_value(self, values: List[float]) -> int:
        # tokens are used as indexes in values by the LLM
        token = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[token]:
                token = i
        return token
