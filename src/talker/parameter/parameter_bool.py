from dataclasses import dataclass

from src.talker.parameter.parameter_str import ParameterStr


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▀▄░█▀█░█▀█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█▀▄░█░█░█░█░█░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀▀░░▀▀▀░▀▀▀░▀▀▀░░
@dataclass()
class TalkerBool(ParameterStr):
    def __post_init__(self) -> None:
        self.prompt = f'''You are a function parameter boolean finder.

Function: {self.function.prototype()}
Query: {self.question}

Respond with JSON:
{self.format_done_parameters()}"{self.to_find}": '''

        self._encode_prompt()
        self.current = f'''{{"{self.to_find}": '''

        # Limit tokens --
        self.authorised_tokens.update(self.llm.encode("true"))
        self.authorised_tokens.update(self.llm.encode("false"))

    # ########################################################################
    # ################################################ END OF JSON FIELD #####
    def is_ended(self) -> bool:
        if self.current == "true" or self.current == "false":
            self.current = self.current + "}"
            return True
        return False
