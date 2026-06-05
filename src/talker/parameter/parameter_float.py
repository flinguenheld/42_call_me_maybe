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
        self.prompt = f""" You are a helpful assistant that call a \
function based on an user query.

Function: {self.function.prototype()}
Description: {self.function.description}
Query: {self.question}

You have to get the value "{self.to_find}"

Respond with a JSON object:
{{"{self.to_find}": """

        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": '''

        # Limit tokens to numbers --
        for i in range(10):
            self.authorised.add(self.llm.token_of(f"{i}"))

        self.authorised.add(self.llm.token_of("."))
        self.authorised.add(self.llm.token_of("-"))

    # ########################################################################
    # ############################################################# TALK #####
    @CallMeError.catch("Talk")
    def talk(self) -> str:
        """Special talk for float.
        Limit logits to 0123456789.-

        Only get two decimals.
        """

        current = self.to_start
        decimals = 0

        for turn in count():
            if decimals > 0 or current[-1] == ".":
                decimals += 1

                if decimals > 2:
                    return current + "}"

            self.printer.up_blah(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)

            token = self._get_token_max_value(logits)
            self.prompt_encoded.append(token)

            decoded = self.llm.decode(token)
            current += decoded
            self.printer.up_blah(5, f"Token: '{decoded}'\n")
            self.printer.up_blah(6, f"{current}\n```")

        raise CallMeError(what="Nothing to say.")
