from dataclasses import dataclass
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀▀░▀░▀░░▀░░░
@dataclass()
class TalkerInt(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only extraction tool. \
Never output anything other than a JSON object.
You have to find a number.
If the number is in plain text, convert in int.
You have to return a int.

Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Extract the value of the parameter: {self.to_find}

Output a single JSON object with exactly one key.

Example:
Sentence: Add 754 to 635 and return the result
Function: fn_how_many(a: int, b: int)
Parameter: b
Output: {{"b": 635}}

Now extract:
Sentence: {self.question}
Function: {self.function.prototype()}
Description: {self.function.description}
Parameter: {self.to_find}
Output:"""
        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": '''

        for i in range(10):
            self.authorised.add(self.llm.token_of(f"{i}"))

        self.authorised.add(self.llm.token_of("-"))
        self.authorised.add(self.llm.token_of("}"))
