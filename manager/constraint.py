from typing import List, Set, Callable
from dataclasses import dataclass, field


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀█░█▀▀░▀█▀░█▀▄░█▀█░▀█▀░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░█░█░█░▀▀█░░█░░█▀▄░█▀█░░█░░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░▀░░▀░▀░▀░▀░▀▀▀░▀░▀░░▀░░░
@dataclass()
class Constraint:
    encode: Callable
    decode: Callable
    current: List[int] = field(default_factory=list)
    authorised_tokens: Set[int] = field(default_factory=set)
    authorised_tokens_2: List[int] = field(default_factory=list)

    def add_current(self, new_token: int) -> None:
        """Add the given token to current buffer."""
        self.current.append(new_token)

    def __str__(self) -> str:
        return "Constraint"
