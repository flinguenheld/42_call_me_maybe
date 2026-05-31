from manager.constraint import Constraint
from typing import List, Any
from llm_sdk import Small_LLM_Model
from utils.utils import print_debug
from dataclasses import dataclass, field
from manager.constraint_function import Constraint_functions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class LLMManager:
    llm: Small_LLM_Model
    question: str
    constraint: Constraint
    debug: bool = False
    prompt: str = ""
    # TODO: ADD IT AS COMMON ATTRIBUTE ????
    prompt_encoded: List[int] = field(default_factory=list)

    _end: int = field(init=False)
    _end_of_text: int = field(init=False)

    def __post_init__(self) -> None:
        self._end = self._token_of("<|im_end|>")
        self._end_of_text = self._token_of("<|endoftext|>")

        print_debug(self.debug, self.llm.get_path_to_vocab_file())
        print_debug(self.debug, self.llm.get_path_to_merges_file())
        print_debug(self.debug, self.llm.get_path_to_tokenizer_file())

    def _token_of(self, who: str) -> int:
        """Get the token of who"""
        return self.llm.encode(who)[0].tolist()[0]

    def _index_max_value(self, values: List[float]) -> int:
        pass

    def next_token(self) -> None:
        pass
