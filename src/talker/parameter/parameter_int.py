from dataclasses import dataclass
from src.talker.parameter.parameter_str import ParameterStr


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀▀░▀░▀░░▀░░░
@dataclass()
class TalkerInt(ParameterStr):
    def __post_init__(self) -> None:
        self.prompt = f'''You are a function parameter integer finder.

Function: {self.function.prototype()}
Query: {self.question}

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": '''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": '''

        # Limit tokens to numbers --
        for i in range(10):
            self.authorised_tokens.add(self.llm.token_of(f"{i}"))

        self.authorised_tokens.add(self.llm.token_of("-"))
        self.authorised_tokens.add(self.llm.token_of("}"))

    # ########################################################################
    # ################################################ END OF JSON FIELD #####
    def is_ended(self) -> bool:
        end = self.current.rfind("}")
        if end > 0:
            self.current = self.current[:end] + "}"
            return True
        return False
