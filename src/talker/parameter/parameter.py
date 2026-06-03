import json
from typing import List
from itertools import count
from json import JSONDecodeError
from dataclasses import dataclass

from src.talker.talker import Talker
from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.visual.visual_printer import VisualPrinter
from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀█░█▀▄░█▀█░█▄█░█▀▀░▀█▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀█░█▀▄░█▀█░█░█░█▀▀░░█░░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerParameter(Talker):
    def update_prompt(
        self,
        function: ModelFunction,
        to_find: str,
    ):
        self.prompt = f"""You are a JSON-only extraction tool. \
Never output anything other than a JSON object.

Sentence: {self.question}
Function: {function.prototype()}
Description: {function.description}
Extract the value of the parameter: {to_find}

Output a single JSON object with exactly one key.

Example:
Sentence: Book a flight to Cardiff for 3 people
Function: fn_go(destination: str)
Parameter: destination
Output: {{"destination": "Cardiff"}}

Now extract:
Sentence: {self.question}
Function: {function.prototype()}
Description: {function.description}
Parameter: {to_find}
Output:"""
        self._encode_prompt()

    def talk(self, parameter: str) -> str:

        current = ""
        to_start = f'''{{"{parameter}": "'''
        to_start_encoded = self.llm.encode(to_start)

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

        return f'{to_start} NO_FOUND"}}'

    @CallMeError.catch("Get arguments")
    def get_arguments(
        self,
        function: ModelFunction,
        output: ModelOutput,
        printer: VisualPrinter,
    ):

        for parameter in function.parameters.keys():
            try:
                printer.up_blah(3, f">Search parameter '{parameter}'")
                self.update_prompt(function, parameter)
                json_arg = json.loads(self.talk(parameter))
                output.parameters[parameter] = json_arg[parameter]

                # TODO add a conversion for numbers ??

            except JSONDecodeError as e:
                raise CallMeError(
                    blah=str(e),
                    prompt=self.prompt,
                    what=f"Can't get the parameter '{parameter}'",
                    why="The returned JSON format is invalid",
                )

            except Exception as e:
                raise CallMeError(
                    what=f"Can't get the parameter '{parameter}'",
                    prompt=self.prompt,
                    error=str(e),
                )
