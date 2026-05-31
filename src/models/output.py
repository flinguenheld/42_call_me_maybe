from typing import Annotated, Dict
from pydantic import BaseModel, Field


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀▄░█▀▀░█░░░░░█▀█░█░█░▀█▀░█▀█░█░█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▀░█░░░░░█░█░█░█░░█░░█▀▀░█░█░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░░▀░░▀░░░▀▀▀░░▀░░░
class ModelOutput(BaseModel):
    prompt: Annotated[str, Field(min_length=3)]
    name: Annotated[str, Field(min_length=3)]
    parameters: Dict[str, Dict[str, str | int | float | bool]]
