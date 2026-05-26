from typing import Annotated
from pydantic import BaseModel, Field

class FunctionDefinitionModel(BaseModel):

    name: Annotated[str, Field(min_length=3)]
    description: Annotated[str, Field(min_length=3)]
    parameters:Annotated[dict[str], Field(min_length=3)]
    returns:
