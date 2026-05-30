from manager.constraint import Constraint
from typing import List, Any
from llm_sdk import Small_LLM_Model
from utils.utils import print_debug
from dataclasses import dataclass, field
from manager.constraint_function import Constraint_functions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass()
class LLMManager:
    llm: Small_LLM_Model
    question: str
    debug: bool
    constraint: Constraint
    prompt: str = ""
    # TODO: ADD IT AS COMMON ATTRIBUTE ????
    prompt_encoded: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._open_brace_token = self._token_of("{")
        self._close_brace_token = self._token_of("}")
        self._quote = self._token_of('"')
        self._colon = self._token_of(":")
        # self.constraint.encode_names(self.llm.encode)

        print_debug(self.debug, self.llm.get_path_to_vocab_file())
        print_debug(self.debug, self.llm.get_path_to_merges_file())
        print_debug(self.debug, self.llm.get_path_to_tokenizer_file())

    def _token_of(self, who: str) -> int | Any:
        """Get the token of who"""
        return self.llm.encode(who)[0].tolist()[0]

    def _index_max_value(self, values: List[float]) -> int:
        pass

    def next_token(self) -> None:
        pass
