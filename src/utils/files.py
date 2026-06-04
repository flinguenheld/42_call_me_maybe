import os
from typing import List
from dataclasses import dataclass, field

from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.models.prompt import ModelPrompt, parse_prompts
from src.models.function_definition import ModelFunction, parse_functions


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░▀█▀░█░░░█▀▀░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░░█░░█░░░█▀▀░▀▀█░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░░
@dataclass
class Files:
    path_prompts: str
    path_functions: str
    path_output: str

    outputs: List[ModelOutput] = field(init=False, default_factory=list)
    prompts: List[ModelPrompt] = field(init=False, default_factory=list)
    functions: List[ModelFunction] = field(init=False, default_factory=list)

    @CallMeError.catch("Init Files")
    def __post_init__(self) -> None:
        self.read_files()

    # ########################################################################
    # ############################################################# READ #####
    @CallMeError.catch("Read files")
    def read_files(self) -> None:
        self.prompts = parse_prompts(self.path_prompts)
        self.functions = parse_functions(self.path_functions)

        os.makedirs(os.path.dirname(self.path_output), exist_ok=True)
        with open(self.path_output, "w"):
            pass

    # ########################################################################
    # ############################################## SAVE OUTPUT IN FILE #####
    def save_output_in_file(self) -> None:
        with open(self.path_output, "w") as file:
            file.write("[")
            file.write(
                ",\n".join(o.model_dump_json(indent=2) for o in self.outputs)
            )
            file.write("]")
