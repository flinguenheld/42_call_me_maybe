import json
from pydantic import BaseModel, Field
from typing import Annotated, Dict, List

from src.error.error import CallMeError


# ░░░░░░░░░░░░░░░░░░░░░█▄█░█▀█░█▀▄░█▀▀░█░░░░░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░
# ░░░░░░░░░░░░░░░░░░░░░█░█░█░█░█░█░█▀▀░█░░░░░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░░
# ░░░░░░░░░░░░░░░░░░░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░░░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░
class ModelFunction(BaseModel):
    name: Annotated[str, Field(min_length=3)]
    description: Annotated[str, Field(min_length=3)]
    parameters: Dict[str, Dict[str, str]]
    returns: Dict[str, str]

    def prototype(self) -> str:
        """Because it's fun"""

        txt = f"{self.name}("
        for key, val in self.parameters.items():
            txt += f"{key}: {val['type']},"
        txt = txt.rstrip(",")
        txt += ") -> "
        for val in self.returns.values():
            txt += f"{val},"

        return txt.rstrip(",")


# ░░░░░░░░░░░░░░░░░█▀█░█▀█░█▀▄░█▀▀░█▀▀░░░█▀▀░█░█░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░█▀▀░░
# ░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀▀█░█▀▀░░░█▀▀░█░█░█░█░█░░░░█░░░█░░█░█░█░█░▀▀█░░
# ░░░░░░░░░░░░░░░░░▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀░░░▀▀▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░▀▀▀░░
@CallMeError.catch("Function definition parser")
def parse_functions(path: str) -> List[ModelFunction]:

    with open(path) as file:
        json_list = json.loads(file.read())
        functions = [ModelFunction.model_validate(func) for func in json_list]
        return functions
