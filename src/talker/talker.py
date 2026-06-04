from typing import List, Set, ClassVar
from dataclasses import dataclass, field

from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.visual.visual_printer import VisualPrinter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░
@dataclass
class Talker:
    MAX_TOKENS_PER_CONV: ClassVar[int] = 50

    question: str
    llm: LLMWrapper
    printer: VisualPrinter
    prompt: str = field(init=False)
    authorised: Set[int] = field(init=False, default_factory=set)
    prompt_encoded: List[int] = field(init=False, default_factory=list)

    # ########################################################################
    # #################################################### ENCODE PROMPT #####
    def _encode_prompt(self) -> None:
        """Used by children for their custom prompt"""

        self.printer.up_prompt(self.prompt)
        self.prompt_encoded = self.llm.encode(self.prompt)

    # ########################################################################
    # ############################################## GET TOKEN MAX VALUE #####
    def _get_token_max_value(self, values: List[float]) -> int:
        """
        Loop in the given logits to find the highest.
        If authorised is not empty, filter token to only authorised ones.

        -> Tokens are used as indexes in values by the LLM.
        """

        token = 0 if not self.authorised else next(iter(self.authorised))

        for i in range(1, len(values) - 1):
            if self.authorised and i not in self.authorised:
                continue

            if values[i] > values[token]:
                token = i
        return token
