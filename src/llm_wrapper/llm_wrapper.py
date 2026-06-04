from __future__ import annotations

from typing import List
from llm_sdk.__init__ import Small_LLM_Model

from src.error.error import CallMeError
from src.utils.debug_printer import DebugPrinter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█▄█░░░█░█░█▀▄░█▀█░█▀█░█▀█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░█░░░█▄█░█▀▄░█▀█░█▀▀░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░░░▀░░░▀▀▀░▀░▀░░
class LLMWrapper:
    """Wrap the given model to easily use methods.
    Allow you to choose between three models:
        - qwen      (Qwen/Qwen3-0.6B)
        - deepseek  (deepseek-ai/deepseek-coder-1.3b-base)
        - lama      (TinyLlama/TinyLlama-1.1B-Chat-v1.0)
    """

    def __init__(self, model_name: str = "Qwen/Qwen3-0.6B"):
        self._llm: Small_LLM_Model = Small_LLM_Model(model_name)

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
    def create_llm(model_name: str = "qwen") -> LLMWrapper:
        try:
            if "deepseek" in model_name:
                return LLMWrapper("deepseek-ai/deepseek-coder-1.3b-base")
            elif "lama" in model_name:
                return LLMWrapper("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
            else:
                return LLMWrapper()

        except Exception:
            raise CallMeError(
                what="Impossible to start the LLM \n(are you connected ?)"
            )
