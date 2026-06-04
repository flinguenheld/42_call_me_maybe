from dataclasses import dataclass

from src.talker.parameter.parameter import TalkerParameter


@dataclass()
class TalkerBool(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool. \
Never output anything other than a JSON object.
You have to find a boolean.
If the boolean is in plain text, convert in boolean.
You have to return a boolean.

Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Extract the value of the parameter: {self.to_find}

Output a single JSON object with exactly one key.

Example:
Sentence: The first door is closed and the second is open
Function: fn_is_valid(a: bool, b: bool)
Parameter: a
Output: {{"a": true}}

Now extract:
Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Parameter: {self.to_find}
Output:"""
        self._encode_prompt()
