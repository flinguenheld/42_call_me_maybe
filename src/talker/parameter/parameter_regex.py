from dataclasses import dataclass
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▄░█▀▀░█▀▀░█▀▀░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▄░█▀▀░█░█░█▀▀░▄▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass()
class TalkerRegex(TalkerParameter):
    def __post_init__(self) -> None:
        #         self.prompt = f"""You are a JSON-only regex extraction tool.
        # Your ONLY job is to extract or build \
        # the regex pattern described in the sentence.
        # Output a single JSON object with exactly one key "regex".
        # The value must be a valid regex pattern string, ready to pass to re.sub().
        # Do NOT add capture groups () unless the sentence explicitly asks for them.
        # Do NOT copy an example pattern — build the correct one for the sentence.

        # GOOD example:
        # Sentence: Replace all digits in the string with X
        # Function: fn_update_string(source: str, regex: str, replacement: str)
        # Parameter: regex
        # Output: {{"regex": "[0-9]+"}}

        # GOOD example:
        # Sentence: Substitute the word 'trumpet' with 'plate' in the string
        # Function: fn_update_string(source: str, regex: str, replacement: str)
        # Parameter: regex
        # Output: {{"regex": "trumpet"}}

        # GOOD example:
        # Sentence: Remove all whitespace characters from the string
        # Function: fn_update_string(source: str, regex: str, replacement: str)
        # Parameter: regex
        # Output: {{"regex": "\\s+"}}

        # Now extract:
        # Sentence: {self.question}
        # Function: {self.function.prototype()}
        # Description: {self.function.description}
        # Parameter: regex
        # Output:{{"{self.to_find}": \""""

        self.prompt = f"""You are a helpful assistant that calls a \
function based on a user query.

Function: {self.function.prototype()}
Query: {self.question}

Get the REGEX.

Respond with a JSON object with ONLY ONE ENTRY:
{{"{self.to_find}": \""""

        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": "'''
