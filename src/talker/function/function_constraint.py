from dataclasses import dataclass, field
from typing import List, Callable, Dict, Set

from src.models.function_definition import ModelFunction


# ░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▄░█▀█░▀█▀░█▀█░▀█▀░░░█▀▀░█░█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░█░░░█░█░█░█░▀▀█░░█░░█▀▄░█▀█░░█░░█░█░░█░░░░█▀▀░█░█░█░█░█░░░░
# ░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░▀░░░░▀░░░▀▀▀░▀░▀░▀▀▀░░
@dataclass
class ConstraintFunction:
    current: List[int] = field(default_factory=list)
    authorised_tokens: Set[int] = field(default_factory=set)
    functions_def: List[ModelFunction] = field(default_factory=list)
    encoded_names: Dict[str, List[int]] = field(default_factory=dict)

    # ########################################################################
    # ############################################ ENCODE FUNCTION NAMES #####
    def encode_names(self, method: Callable) -> None:
        """Fill the encoded_names dict with name:tokens"""
        for function in self.functions_def:
            self.encoded_names[function.name] = method(function.name)

    # ########################################################################
    # ####################################################### LAST ONE ? #####
    def get_final_choice(self) -> ModelFunction | None:
        """The constrain mechanism is done when only one choice left.
        Get and return the model when time has come!
        """
        if len(self.encoded_names) == 1:
            last = next(iter(self.encoded_names.keys()))
            for model in self.functions_def:
                if model.name == last:
                    return model

        return None

    # ########################################################################
    # ###################################################### ADD CURRENT #####
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

    # ########################################################################
    # #################################################### UP AUTHORISED #####
    def update_authorised_tokens(self, column: int) -> None:
        """Get the token of all encoded name at the 'column' position"""
        self.authorised_tokens.clear()
        for tokens in self.encoded_names.values():
            if column < len(tokens):
                self.authorised_tokens.add(tokens[column])

    # ########################################################################
    # ############################################################## STR #####
    def __str__(self) -> str:
        """Return a formated string with all function name
        and their description.

        Used in the prompt.
        """
        text = ""
        for function in self.functions_def:
            text += f"- {function.name}: {function.description}\n"

        return text
