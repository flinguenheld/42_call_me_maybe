from typing import List
from dataclasses import dataclass, field
from llm_sdk.__init__ import Small_LLM_Model

from src.utils.utils import print_debug


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█░█░█▀▄░█▀█░█▀█░█▀█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█▄█░█▀▄░█▀█░█▀▀░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░░░▀░░░▀▀▀░▀░▀░░
@dataclass()
class LLMWrapper:
    _llm: Small_LLM_Model = field(init=False)
    end: int = field(init=False)
    end_of_text: int = field(init=False)

    def __post_init__(self) -> None:
        self._llm = Small_LLM_Model()
        self.end = self.token_of("<|im_end|>")
        self.end_of_text = self.token_of("<|endoftext|>")

    def encode(self, who: str) -> List[int]:
        return list[int](self._llm.encode(who)[0].tolist())

    def token_of(self, who: str) -> int:
        return self.encode(who)[0]

    def decode(self, who: int | List[int]) -> str:
        if isinstance(who, int):
            return str(self._llm.decode([who]))
        else:
            return str(self._llm.decode(who))

    def get_logits(self, tokens: List[int]) -> List[float]:
        return list[float](self._llm.get_logits_from_input_ids(tokens))

    def print_paths(self, debug: bool) -> None:
        print_debug(debug, self._llm.get_path_to_vocab_file())
        print_debug(debug, self._llm.get_path_to_merges_file())
        print_debug(debug, self._llm.get_path_to_tokenizer_file())
