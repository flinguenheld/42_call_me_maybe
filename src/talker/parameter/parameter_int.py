from dataclasses import dataclass
from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀▀░▀░▀░░▀░░░
@dataclass()
class TalkerInt(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f""" You are a helpful assistant that call a \
function based on an user query.

Function: {self.function.prototype()}
Description: {self.function.description}
Query: {self.question}

You have to get the value "{self.to_find}"

Respond with a JSON object:
{{"{self.to_find}": """

        self._encode_prompt()
        self.to_start = f'''{{"{self.to_find}": '''

        # Limit tokens to numbers --
        for i in range(10):
            self.authorised.add(self.llm.token_of(f"{i}"))

        self.authorised.add(self.llm.token_of("-"))
        self.authorised.add(self.llm.token_of("}"))
