from typing import List
from dataclasses import dataclass, field
from llm_wrapper.llm_wrapper import LLMWrapper


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class LLMManager:
    debug: bool
    question: str
    llm: LLMWrapper
    _prompt: str = field(init=False)
    _prompt_encoded: List[int] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.llm.print_paths(self.debug)

    def _index_max_value(self, values: List[float]) -> int:
        pass

    def next_token(self) -> None:
        pass
