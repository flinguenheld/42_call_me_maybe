from dataclasses import dataclass
from src.talker.parameter.parameter_str import ParameterStr


# ░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀█░█▀▄░█▀█░█▀█░█▀▀░█▀▄░█▀▀░█▀█░█▀▄░█▀▀░█▀▄░░
# ░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█▀▄░█░█░█░█░█▀▀░█▀▄░█▀▀░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀░▀░▀▀▀░▀▀▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀░░▀▀▀░▀░▀░░
@dataclass()
class TalkerJSONProofreader(ParameterStr):
    def __post_init__(self) -> None:
        self.prompt = f'''You are a JSON proofreader.

This JSON has an invalid format:
{self.question}

- Search the error.
- Rewrite it:

{{"{self.to_find}": '''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": '''
