from typing import List
from itertools import count
from dataclasses import dataclass

from src.error.error import CallMeError
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▀░█░░░█▀█░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█░░░█░█░█▀█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░░
@dataclass()
class TalkerFloat(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f'''You float finder.

Function: {self.function.prototype()}
Query: {self.question}

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": '''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": '''

        # Limit tokens to numbers --
        for i in range(10):
            self.authorised_tokens.add(self.llm.token_of(f"{i}"))

        self.authorised_tokens.add(self.llm.token_of("."))
        self.authorised_tokens.add(self.llm.token_of("-"))

    # ########################################################################
    # ############################################################# TALK #####
    @CallMeError.catch("Talk")
    def talk(self) -> str:
        """Special talk for float.
        Limit logits to 0123456789.-

        Only get two decimals.
        """

        decimals = 0
        for turn in count():
            # ### End of field ? ##########################
            if decimals > 0 or self.current[-1] == ".":
                decimals += 1
                if decimals > 2:
                    return self.current + "}"

            self.printer.blah_up(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)

            token = self._get_token_max_value(logits)
            self.prompt_encoded.append(token)

            decoded = self.llm.decode(token)
            self.current += decoded
            self.printer.blah_up(5, f"Token: '{decoded}'\n")
            self.printer.blah_up(6, f"{self.current}\n```")
            self.printer.blah_save_log(self.current)

        raise CallMeError(what="Nothing to say.")
