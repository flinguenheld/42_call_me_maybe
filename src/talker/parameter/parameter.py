from itertools import count
from typing import List, Dict
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
    current: str = field(init=False)
    done_parameters: Dict[str, str | int | float | bool]

    # ########################################################################
    # ########################################################### PROMPT #####
    def __post_init__(self) -> None:
        self.prompt = f'''You argument finder.

Function: {self.function.prototype()}
Query: {self.question}

Find "{self.to_find}".

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": "'''

        self.current = f'''{{"{self.to_find}": "'''
        self._encode_prompt()

    # ########################################################################
    # #################################################### ALREADY FOUND #####
    def format_done_parameters(self) -> str:
        """Format done parameters in a (non finished) one line JSON"""
        already = "{"
        if self.done_parameters:
            for param, argument in self.done_parameters.items():
                if isinstance(argument, (int, float, bool)):
                    already += f'''"{param}": {argument}, '''
                else:
                    already += f'''"{param}": "{argument}", '''
            return already
        else:
            return already

    # ########################################################################
    # ################################################ END OF JSON FIELD #####
    def get_end(self, current: str) -> int:
        return max(
            current.rfind('", '),
            current.rfind('",\n'),
            current.rfind('"}'),
        )

    # ########################################################################
    # ############################################################# TALK #####
    @CallMeError.catch("Talk")
    def talk(self) -> str:
        """Common talk method for parameters.

        Talk to the LLM, filter and save the returned tokens.
        Apply restrictions if 'self.authorised' has been filled.

        Return only one JSON value with one field.
        Stop when the last validated token is the end of the field.
        """

        for turn in count():
            self.printer.blah_up(4, f"```json\nturn {turn}\n\n")
            logits: List[float] = self.llm.get_logits(self.prompt_encoded)

            if turn > self.TOKEN_MAX:
                raise CallMeError(what=f"Token limit ({self.TOKEN_MAX}).")

            token = self._get_token_max_value(logits)
            self.prompt_encoded.append(token)

            decoded = self.llm.decode(token)
            self.current += decoded
            self.printer.blah_up(5, f"Token: '{decoded}'\n")
            self.printer.blah_up(6, f"{self.current}\n```")
            self.printer.blah_save_log(self.current)

            # ### End of field ? ##########################
            end = self.get_end(self.current)
            if end > 0:
                return self.current[:end] + '"}'

        raise CallMeError(what="Nothing to say.")
