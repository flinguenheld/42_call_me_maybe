from typing import List, Set
from itertools import count
from dataclasses import dataclass, Field, field

from src.talker.talker import Talker
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▄░█▀█░█▄█░█▀▀░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀█░█▀▄░█▀█░█░█░█▀▀░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerParameter(Talker):
    function: ModelFunction
    to_find: str
    to_start: str = field(init=False)
    not_found: str = field(init=False)

    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool. \
Never output anything other than a JSON object.
You have to find a string.
You have to return a string.

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
        self.not_found = f'''{{"{self.to_find}": "NOT FOUND"}}'''
        self._encode_prompt()

    def talk(self) -> str:

        current = ""
        to_start_encoded = self.llm.encode(self.to_start)

        for turn in count():
            self.printer.up_blah(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self._prompt_encoded)

            # Skip the first turns --
            # I tried to directly add it in the prompt but it looks better
            # to call get_logit token per token -_-
            if turn < len(to_start_encoded):
                current += self.llm.decode(to_start_encoded[turn])
                self._prompt_encoded.append(to_start_encoded[turn])

            elif turn > 50:
                break

            else:
                token = self._get_token_max_value(logits)

                self._prompt_encoded.append(token)
                current += self.llm.decode(token)

                if current.rstrip()[-1] == "}":
                    return current.rstrip()

            self.printer.up_blah(5, f"{current}\n```")

        return self.not_found
