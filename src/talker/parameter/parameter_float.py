from dataclasses import dataclass
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▀░█░░░█▀█░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▀░█░░░█░█░█▀█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░░░▀▀▀░▀▀▀░▀░▀░░▀░░░
@dataclass()
class TalkerFloat(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f"""You are a JSON-only parameter extraction tool.
Your ONLY job is to copy the number that appears \
in the sentence into the output.
Do NOT solve, compute, or evaluate. Do NOT output the answer to the question.
The sentence is a QUESTION, not a computation. \
Extract the INPUT, not the RESULT.
If the value is written as words (e.g. "five"), convert it to a float.

Function: {self.function.prototype()}
Description: {self.function.description}
Sentence: {self.question}

GOOD example:
Sentence: What is the square root of 9025?
Function: fn_square_root(a: float)
Parameter: a
Output: {{"a": 9025.0}}

BAD example (do NOT do this):
Sentence: What is the square root of 9?
Function: fn_square_root(a: float)
Parameter: a
Output: {{"a": 3.0}}  <- WRONG: 3 is the computed result, not the input value

GOOD example:
Sentence: What is the sum of 54 and 154?
Function: fn_add_numbers(a: float, b: float)
Parameter: a
Output: {{"a": 54.0}}

BAD example (do NOT do this):
Sentence: What is the sum of 26 and 13?
Function: fn_add_numbers(a: float, b: float)
Parameter: a
Output: {{"a": 40.0}}  <- WRONG: 40 is the computed result, not the value of a

GOOD example:
Sentence: Add 754 to 635 and return the result
Function: fn_how_many(a: float, b: float)
Parameter: b
Output: {{"b": 635.0}}

Now extract — do NOT compute, just copy the number from the sentence:
Sentence: {self.question}
Function: {self.function.prototype()}
Parameter: {self.to_find}
Output:"""

        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": '''

        # Limit tokens to numbers --
        for i in range(10):
            self.authorised.add(self.llm.token_of(f"{i}"))

        self.authorised.add(self.llm.token_of("-"))
        self.authorised.add(self.llm.token_of("."))
        self.authorised.add(self.llm.token_of("}"))
