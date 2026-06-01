from typing import Dict
from dataclasses import dataclass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀▄░█▀▀░█░░░░░█▀█░█░█░▀█▀░█▀█░█░█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▀░█░░░░░█░█░█░█░░█░░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░░▀░░▀░░░▀▀▀░░▀░░░


@dataclass
class ModelOutput:
    prompt: str
    name: str
    parameters: Dict[str, str]
