from typing import List
from itertools import count
from dataclasses import dataclass, field

from src.talker.talker import Talker
from src.error.error import CallMeError
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▄░█▀█░█▄█░█▀▀░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀█░█▀▄░█▀█░█░█░█▀▀░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerParameter(Talker):
    function: ModelFunction
    to_find: str
    to_start: str = field(init=False)

    # ########################################################################
    # ########################################################### PROMPT #####
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool. \
Never output anything other than a JSON object.
You have to find a string.
You have to return a string.
Double all backslash.

Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Extract the value of the parameter: {self.to_find}

Output a single JSON object with exactly one key.

Example:
Sentence: Book a flight to Cardiff for 3 people
Function: fn_go(destination: str)
Parameter: destination
Output: {{"destination": "Cardiff"}}

Now extract:
Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Parameter: {self.to_find}
Output:"""

        self.to_start = f'''{{"{self.to_find}": "'''
        self._encode_prompt()

    # ########################################################################
    # ############################################################# TALK #####
    @CallMeError.catch("Talk")
    def talk(self) -> str:
        """Common talk method for parameters.

        Talk to the LLM, filter and save the returned tokens.
        Apply two restrictions:
            - On the beginning with 'self.to_start'
            - On the other tokens if 'self.authorised' has been filled

        Return only one JSON value.
        Stop when the last validated token ends with '}'.
        """

        current = ""
        to_start_encoded = self.llm.encode(self.to_start)

        for turn in count():
            self.printer.up_blah(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)

            # Skip the first turns with to_start --
            # I tried to directly add it in the prompt but it looks better
            # to call get_logit token per token -_-
            if turn < len(to_start_encoded):
                current += self.llm.decode(to_start_encoded[turn])
                self.prompt_encoded.append(to_start_encoded[turn])

            elif turn > self.MAX_TOKENS_PER_CONV:
                raise CallMeError(
                    what=f"Token limit reached ({self.MAX_TOKENS_PER_CONV})."
                )

            else:
                token = self._get_token_max_value(logits)

                self.prompt_encoded.append(token)
                current += self.llm.decode(token)

                if current.rstrip()[-1] == "}":
                    return current.rstrip()

            self.printer.up_blah(5, f"{current}\n```")

        raise CallMeError(what="Nothing to say.")
