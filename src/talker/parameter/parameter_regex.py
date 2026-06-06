from dataclasses import dataclass
from src.talker.parameter.parameter_str import ParameterStr


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▄░█▀▀░█▀▀░█▀▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▄░█▀▀░█░█░█▀▀░▄▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass()
class TalkerRegex(ParameterStr):
    def __post_init__(self) -> None:
        self.prompt = f'''You regular expression finder.

Function: {self.function.prototype()}
Query: {self.question}

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": "'''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": "'''
