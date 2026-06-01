from typing import Dict
from pydantic import BaseModel


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀▄░█▀▀░█░░░░░█▀█░█░█░▀█▀░█▀█░█░█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▀░█░░░░░█░█░█░█░░█░░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░░▀░░▀░░░▀▀▀░░▀░░░
class ModelOutput(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, str | int | float | bool]
