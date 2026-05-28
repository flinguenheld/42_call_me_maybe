from typing import List, Any
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from models.prompt import parse_prompts
from models.function_definition import (
    # FunctionDefinition,
    parse_functions,
)
from parser_call_me import parse_call_me
from termcolor import cprint
from error.error import CallMeError


@dataclass()
class LLMManager:
    prompt: str
    llm: Small_LLM_Model = Small_LLM_Model()

    def __post_init__(self) -> None:
        self._open_brace_token = self._index_of("{")
        self._close_brace_token = self._index_of("}")
        self._quote = self._index_of('"')
        self._colon = self._index_of(":")
        self._answer_tokens: List[int] = []
        self._prompt_tokens = self.llm.encode(self.prompt)[0].tolist()
        self._prompt_tokens.append(self._open_brace_token)

    def _index_of(self, who: str) -> int | Any:
        """Get the index of who (works for one char)"""
        return self.llm.encode(who)[0].tolist()[0]

    def _index_max_value(self, values: List[float]) -> int:
        """Get the index of the maximum value"""
        index = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[index]:
                index = i

        print(f"index found: {index} -> {len(values)}")
        return index

    def next_token(self) -> None:

        logits: List[float] = self.llm.get_logits_from_input_ids(
            self._prompt_tokens
        )
        # Get the index of the maximum
        maxi = self._index_max_value(logits)

        print(f"maxi found: {maxi} -> Decoded -> '{self.llm.decode([maxi])}'")
        self._prompt_tokens.append(maxi)


if __name__ == "__main__":
    arguments = parse_call_me()

    if not arguments:
        cprint("\nPlease respect the arguments", "red", attrs=["blink"])
        exit(1)
    else:
        try:
            model = parse_functions(arguments["definitions"])
            prompts = parse_prompts(arguments["input"])

            llm = LLMManager("What is the sum of 2 and 3?")
            for _ in range(10):
                llm.next_token()

        except CallMeError as e:
            e.print()
