import json
from typing import List, Dict
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
    found_parameters: Dict[str, str | int | float | bool]

    # ########################################################################
    # ########################################################### PROMPT #####
    def __post_init__(self) -> None:

        self.prompt = f"""You are a helpful assistant that calls a \
function based on a user query.

Function: {self.function.prototype()}
Query: {self.question}

Get "{self.to_find}". Do NOT transform.

Respond with a JSON object with ONLY ONE ENTRY:
{{"{self.to_find}": \""""

        self.to_start = f'''{{"{self.to_find}": "'''
        self._encode_prompt()

    # TODO REMOVE THAT ---------------------------
    # TODO REMOVE THAT ---------------------------
    # TODO REMOVE THAT ---------------------------
    # TODO REMOVE THAT ---------------------------
    # ########################################################################
    # #################################################### ALREADY FOUND #####
    def format_already_found(self) -> str:
        already = ""
        if self.found_parameters:
            # already = f"Known: {json.dumps(self.found_parameters)}"
            already = "Already found:\n"
            for param, argument in self.found_parameters.items():
                if isinstance(argument, int) or isinstance(argument, float):
                    already += f"- {param}: {argument}\n"
                else:
                    already += f"- {param}: {argument}\n"

        return already

    # ########################################################################
    # ############################################################# TALK #####
    @CallMeError.catch("Talk")
    def talk(self) -> str:
        """Common talk method for parameters.

        Talk to the LLM, filter and save the returned tokens.
        Apply restrictions if 'self.authorised' has been filled

        Return only one JSON value.
        Stop when the last validated token is the end of the field.
        """

        current = self.to_start

        for turn in count():
            self.printer.up_blah(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)

            if turn > self.MAX_TOKENS_PER_CONV:
                raise CallMeError(
                    what=f"Token limit reached ({self.MAX_TOKENS_PER_CONV})."
                )

            token = self._get_token_max_value(logits)

            self.prompt_encoded.append(token)

            decoded = self.llm.decode(token)
            current += decoded
            self.printer.up_blah(5, f"Token: '{decoded}'\n")

            # Check the end of the field
            if decoded == '",' and current[-3] != "\\":
                return current.rstrip()[:-1] + "}"

            if decoded == '"}\n' and current[-4] != "\\":
                return current.rstrip()

            if current.rstrip()[-4:] == '", "':
                return current[:-3] + "}"

            if current.rstrip()[-2:] == '",' and current.rstrip()[-3] != "\\":
                return current.rstrip()[:-1] + "}"

            if current.rstrip()[-1] == "}" and current.rstrip()[-2] != "\\":
                return current.rstrip()

            self.printer.up_blah(6, f"{current}\n```")

        raise CallMeError(what="Nothing to say.")
