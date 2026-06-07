import json
from typing import Any
from json import JSONDecodeError
from dataclasses import dataclass

from src.utils.files import Files
from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.visual.visual_printer import VisualPrinter
from src.models.function_definition import ModelFunction

from src.talker.function.function import TalkerFunction
from src.talker.parameter.parameter_int import TalkerInt
from src.talker.parameter.parameter_bool import TalkerBool
from src.talker.parameter.parameter_str import ParameterStr
from src.talker.parameter.parameter_regex import TalkerRegex
from src.talker.parameter.parameter_float import TalkerFloat
from src.talker.parameter.parameter_invalid import TalkerProofreader


# ░░░░░░░░░░░░░░░░░░░░░▀█▀░█▀█░█░░░█░█░█▀▀░█▀▄░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░█░░█▀█░█░░░█▀▄░█▀▀░█▀▄░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█▀▄░░
# ░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░░
@dataclass
class TalkerManager:
    llm: LLMWrapper
    files: Files
    printer: VisualPrinter

    # ########################################################################
    # ################################################ MANAGE ONE PROMPT #####
    @CallMeError.catch("Manage prompt")
    def manage_one_prompt(self, prompt: str) -> None:

        output = ModelOutput.model_construct()
        output.prompt = prompt
        output.parameters = {}

        self.printer.prompt_list_up(prompt)
        self.printer.blah_up(1, ">Search function...\n")
        talker_function = TalkerFunction(
            llm=self.llm,
            question=prompt,
            functions=self.files.functions,
            printer=self.printer,
        )

        talker_function.talk()
        if talker_function.found:
            functi = talker_function.found
            output.name = functi.name
            self.printer.blah_up(1, ">Function found\n")
            self.printer.blah_up(2, f"```python\n{functi.prototype()}\n```\n")
            self.get_all_arguments(functi, output)
        else:
            output.name = "Error: No function found"

        self.files.outputs.append(output)

    # ########################################################################
    # ################################################ GET ALL ARGUMENTS #####
    def get_all_arguments(
        self,
        function: ModelFunction,
        output: ModelOutput,
    ) -> None:
        """Loop in the given function's parameters to ask
        the LLM to find their arguments one by one.
        Then update the given output.

        Can be used for:
           - str
           - float
           - int
           - bool
           - regex

        If the returned json format is incorect, ask the LLM to fix it.
        If it still fails, set the argument as 'ERROR: ...' and continue"""

        for param, values in function.parameters.items():
            try:
                self.printer.blah_up(3, f">Search parameter '{param}'")

                # Specialise the talker --
                talker_class = ParameterStr
                if param.lower() == "regex":
                    talker_class = TalkerRegex
                else:
                    match values["type"]:
                        case "number" | "float":
                            talker_class = TalkerFloat
                        case "integer" | "int":
                            talker_class = TalkerInt
                        case "boolean" | "bool":
                            talker_class = TalkerBool

                talker = talker_class(
                    llm=self.llm,
                    to_find=param,
                    function=function,
                    printer=self.printer,
                    question=output.prompt,
                    done_parameters=output.parameters,
                )

                json_arg = self.proofread(talker.talk(), param, function)
                output.parameters[param] = json_arg[param]

            except JSONDecodeError as e:
                output.parameters[param] = f"ERROR: Invalid JSON -> '{e}'"

            except CallMeError as e:
                output.parameters[param] = f"ERROR: {e.context['what']}"

            except Exception as e:
                output.parameters[param] = f"ERROR: {str(e)}"

    # ########################################################################
    # ################################################### JSON PROOFREAD #####
    def proofread(self, llm_words: str, param: str, fun: ModelFunction) -> Any:
        """Convert llm_words into a json dict.
        If it fails, launchs a special talker.
        It will asks the llm to fix the given JSON.
        If it's still wrong, raise a JSONDecodeError.
        """

        try:
            return json.loads(llm_words)

        except JSONDecodeError:
            talker = TalkerProofreader(
                llm=self.llm,
                to_find=param,
                question=llm_words,
                function=fun,  # Not used
                done_parameters={},
                printer=self.printer,
            )

            llm_words = talker.talk()
            return json.loads(llm_words)
