from models.function_definition import FuncDef
from typing import List, Set, Callable, Dict
from dataclasses import dataclass, field


@dataclass()
class Constraint_functions:
    functions_def: List[FuncDef]
    current: List[int] = field(default_factory=list)
    authorised_tokens: Set[int] = field(default_factory=set)
    encoded_names: Dict[str, List[int]] = field(default_factory=dict)
    index: int = -1

    def encode_names(self, method: Callable) -> None:
        """Fill the encoded_names dict with name:tokens"""
        for function in self.functions_def:
            self.encoded_names[function.name] = method(function.name)[
                0
            ].tolist()

    def get_final_choice(self) -> str | None:
        """The constrain mechanism is done when only one choice left.
        So return it only when it's the case
        """
        if len(self.encoded_names) == 1:
            return next(iter(self.encoded_names.keys()))

        return None

    def add_current(self, new_token: int) -> None:
        """Add the given token to current buffer.
        Then filter the encoded_names to keep only those
        which start with current.
        """
        self.current.append(new_token)

        new_dict = {}
        for function, tokens in self.encoded_names.items():
            if len(self.current) > len(tokens):
                continue

            start_with = True
            for a, b in zip(self.current, tokens):
                if a != b:
                    start_with = False
                    break

            if start_with:
                new_dict[function] = tokens

        self.encoded_names = new_dict

    def next_column(self) -> None:
        """Move forward and update the authorised_token with the next 'column'
        of all encoded names
        """
        self.index += 1
        self.authorised_tokens.clear()
        for tokens in self.encoded_names.values():
            if self.index < len(tokens):
                self.authorised_tokens.add(tokens[self.index])

    def __str__(self) -> str:
        """Return a formated string with all function name
        and their description
        """
        text = ""
        for function in self.functions_def:
            text += f"- {function.name}: {function.description}\n"

        return text
