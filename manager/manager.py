from typing import List, Any
from dataclasses import dataclass
from llm_sdk import Small_LLM_Model
from manager.constraint import Constraint


@dataclass()
class LLMManager:
    prompt: str
    constraint: Constraint
    llm: Small_LLM_Model = Small_LLM_Model()

    def __post_init__(self) -> None:
        self._open_brace_token = self._index_of("{")
        self._close_brace_token = self._index_of("}")
        self._quote = self._index_of('"')
        self._colon = self._index_of(":")
        self._answer_tokens: List[int] = []
        self._prompt_tokens = self.llm.encode(self.prompt)[0].tolist()

        self.constraint.encode_names(self.llm.encode)
        print(self.constraint.encoded)

        self._real_prompt = f"""
You are a function calling assistant. Given the following available functions:
{self.constraint}
User request: "{self.prompt}"
Find the correct function.
Give only the FUNCTION NAME:
function: """
        self._real_prompt_encoded = self.llm.encode(self._real_prompt)[
            0
        ].tolist()
        print(f"prompt: '{self._real_prompt}'")
        # print(f"prompt: '{self._real_prompt_encoded}'")
        # self._prompt_tokens.append(self._open_brace_token)

    def _index_of(self, who: str) -> int | Any:
        """Get the index of who (works for one char)"""
        return self.llm.encode(who)[0].tolist()[0]

    def _is_number(self, token: int) -> bool:
        return self.llm.decode([token]).isdigit()

    def _index_max_value(self, values: List[float]) -> int:
        """Get the index of the maximum value"""

        print("=== look for logits ===")
        print(self.constraint.authorised_tokens)
        print(self.llm.decode([t for t in self.constraint.authorised_tokens]))
        print("=======================")

        index = next(iter(self.constraint.authorised_tokens))
        for i in range(1, len(values) - 1):
            if (
                i in self.constraint.authorised_tokens
                and values[i] > values[index]
            ):
                print(f"here: {i} -> {self.llm.decode([i])} -> {values[i]}")
                index = i

        # print(f"index found: {index} -> {len(values)}")
        return index

    def next_token(self) -> None:

        turn = 0
        while True:
            # FIND A WAY TO SKIP WHEN THERE IS JUST ONE CHOICE LEFT
            print(f"------------------------------------ trun {turn} ----")
            turn += 1

            # Get the index of the maximum
            self.constraint.next_index()
            if len(self.constraint.authorised_tokens) == 0:
                print(f"FOUND : {self.llm.decode(self.constraint.selected)}")
                break

            logits: List[float] = self.llm.get_logits_from_input_ids(
                self._real_prompt_encoded
            )

            maxi = self._index_max_value(logits)
            print(
                f"maxi found: {maxi} -> Decoded -> '{self.llm.decode([maxi])}'"
            )
            # print(self.llm.decode([maxi]), end="")
            # print(self.llm.decode([maxi]))
            self.constraint.add_selected(maxi)

            self._real_prompt_encoded.append(maxi)
