from models.function_definition import FuncDef
from typing import List, Set, Callable, Dict
from dataclasses import dataclass, field


@dataclass()
class Constraint:
    functions_def: List[FuncDef]
    encoded: Dict[str, List[int]] = field(default_factory=dict)

    def __post_init__(self):
        self.names = [fun.name for fun in self.functions_def]
        self.index = -1
        self.authorised_tokens: Set[int] = set()
        self.selected: List[int] = []

    def encode_names(self, method: Callable):
        for function in self.functions_def:
            self.encoded[function.name] = method(function.name)[0].tolist()

    def add_selected(self, new_token: int):
        self.selected.append(new_token)
        current: str = "".join((str(i) for i in self.selected))

        new_dict = {}
        for function, tokens in self.encoded.items():
            t: str = "".join((str(i) for i in tokens))
            if t.startswith(current):
                new_dict[function] = tokens

        self.encoded = new_dict

    def next_index(self):
        self.index += 1
        self.authorised_tokens.clear()
        for tokens in self.encoded.values():
            if self.index < len(tokens):
                self.authorised_tokens.add(tokens[self.index])

    def __str__(self):
        text = ""
        for function in self.functions_def:
            text += f"- {function.name}: {function.description}\n"

        return text
