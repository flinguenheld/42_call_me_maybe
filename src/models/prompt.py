import json
from typing import Annotated, List
from pydantic import BaseModel, Field

from src.error.error import CallMeError


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀▄░█▀▀░█░░░░░█▀█░█▀▄░█▀█░█▄█░█▀█░▀█▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▀░█░░░░░█▀▀░█▀▄░█░█░█░█░█▀▀░░█░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀░░░▀░▀░▀▀▀░▀░▀░▀░░░░▀░░░
class ModelPrompt(BaseModel):
    text: Annotated[str, Field(min_length=3, alias="prompt")]


@CallMeError.catch("Input, prompt parser")
def parse_prompts(path: str) -> List[ModelPrompt]:

    with open(path) as file:
        json_list = json.loads(file.read())
        prompts = [ModelPrompt.model_validate(func) for func in json_list]
        return prompts
