from dataclasses import dataclass

from src.talker.parameter.parameter import TalkerParameter


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▄░█▀█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▄░█░█░█░█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀▀▀░▀▀▀░░
@dataclass()
class TalkerBool(TalkerParameter):
    def __post_init__(self) -> None:
        self.prompt = f'''You boolean finder.

Function: {self.function.prototype()}
Query: {self.question}

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": '''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": '''

        # Limit tokens --
        self.authorised_tokens.update(self.llm.encode("true"))
        self.authorised_tokens.update(self.llm.encode("false"))
