from dataclasses import dataclass
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▄░█▀▀░█▀▀░█▀▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▄░█▀▀░█░█░█▀▀░▄▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass()
class TalkerRegex(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool. \
Output a single JSON object with exactly one key.
Extract a regex pattern as JSON. Output only a JSON object, nothing else.

Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Extract the value of the parameter: regex

Output a single JSON object with exactly one key.

Example:
Sentence: Replace all vowels in 'hello baby' with hyphen
description: Replace all occurrences matching a regex pattern in a string
Function: fn_update_string(source: str, regex: str: replacement: str)
Parameter: regex
Output: {{"regex": "aeiouAEIOU"}}

Output:"""

        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": "'''
