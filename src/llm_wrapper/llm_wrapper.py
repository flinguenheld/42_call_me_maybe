from __future__ import annotations

from typing import List
from dataclasses import dataclass
from llm_sdk.__init__ import Small_LLM_Model

from src.error.error import CallMeError
from src.utils.debug_printer import DebugPrinter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█░█░█▀▄░█▀█░█▀█░█▀█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█▄█░█▀▄░█▀█░█▀▀░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░░░▀░░░▀▀▀░▀░▀░░
@dataclass()
class LLMWrapper:
    _llm: Small_LLM_Model = Small_LLM_Model()

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

    # ########################################################################
    # ############################################################ PATHS #####
    def paths(self) -> str:
        # flake8: noqa: W291
        return f"""> vocab:     {self._llm.get_path_to_vocab_file()}  
                   > merges:    {self._llm.get_path_to_merges_file()}  
                   > tokenizer: {self._llm.get_path_to_tokenizer_file()}  
                   """
        # flake8: enable=W291

    def print_paths(self, printer: DebugPrinter) -> None:
        printer.print(self._llm.get_path_to_vocab_file())
        printer.print(self._llm.get_path_to_merges_file())
        printer.print(self._llm.get_path_to_tokenizer_file())

    # ########################################################################
    # ########################################################### CREATE #####
    @staticmethod
    def create_llm() -> LLMWrapper:
        try:
            return LLMWrapper()
        except Exception:
            raise CallMeError(
                what="Impossible to start the LLM \n(are you connected ?)"
            )
