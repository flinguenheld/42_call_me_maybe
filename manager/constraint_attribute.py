from typing import List, Callable, Dict
from dataclasses import dataclass, field
from manager.constraint import Constraint
from models.function_definition import FuncDef


@dataclass()
class Constraint_Attribute(Constraint):
    def add_numbers_as_authorised(self, prompt: str):
        # TODO: CAN'T USE A SET HERE, USE A LIST AN REMOVE WHEN SELECTED
        # TODO: CAN'T USE A SET HERE, USE A LIST AN REMOVE WHEN SELECTED
        # TODO: CAN'T USE A SET HERE, USE A LIST AN REMOVE WHEN SELECTED
        # TODO: CAN'T USE A SET HERE, USE A LIST AN REMOVE WHEN SELECTED
        # TODO: CAN'T USE A SET HERE, USE A LIST AN REMOVE WHEN SELECTED
        for token in self.encode(prompt):
            if self.decode(token).isdigit():
                self.authorised_tokens.add(token)

        # In the prompt, get all tokens
        # Keep only those which are numbers
