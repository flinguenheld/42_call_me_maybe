from dataclasses import dataclass

from src.talker.parameter.parameter import TalkerParameter


@dataclass()
class TalkerInt(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool.
Output a single JSON object with exactly one key.
Extract an integer parameter from the sentence.
If the value is written as text, convert it to a digit.

Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Extract the value of the parameter: {self.to_find}

Examples:
Sentence: Add 546 to 102 and return the result
Function: fn_how_many(a: int, {self.to_find}: int)
Parameter: {self.to_find}
Output: {{"{self.to_find}": 102}}

Sentence: Repeat the word 'hello' five times
Function: fn_repeat(word: str, {self.to_find}: int)
Parameter to extract: {self.to_find}
Output: {{"{self.to_find}": 5}}

Output:"""
        self._encode_prompt()
