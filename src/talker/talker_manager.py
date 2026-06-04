import json
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
from src.talker.parameter.parameter import TalkerParameter
from src.talker.parameter.parameter_regex import TalkerRegex
from src.talker.parameter.parameter_float import TalkerFloat


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

        self.printer.up_prompt_list(prompt)
        self.printer.up_blah(1, ">Search function...\n")
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
            self.printer.up_blah(1, ">Function found\n")
            self.printer.up_blah(2, f"```python\n{functi.prototype()}\n```\n")
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
        """Loop in the given function's parameters to ask the LLM to find their
        arguments one by one.
        Then update the given output.

        Can be used for:
           - str
           - float
           - int
           - bool
           - regex

        Do not stop if error, set the arguement as 'ERROR: ...' and continue"""

        for parameter, value in function.parameters.items():
            try:
                self.printer.up_blah(3, f">Search parameter '{parameter}'")
                llm_words: str = ""

                # Specialise the talker --
                talker_class = TalkerParameter
                if parameter.lower() == "regex":
                    talker_class = TalkerRegex
                else:
                    match value["type"]:
                        case "number" | "float":
                            talker_class = TalkerFloat
                        case "integer" | "int":
                            talker_class = TalkerInt
                        case "boolean" | "bool":
                            talker_class = TalkerBool

                talker = talker_class(
                    output.prompt,
                    self.llm,
                    self.printer,
                    function,
                    parameter,
                )

                llm_words = talker.talk()
                json_arg = json.loads(llm_words.replace("\\", "\\\\"))
                output.parameters[parameter] = json_arg[parameter]

            except JSONDecodeError:
                output.parameters[
                    parameter
                ] = f'''"ERROR: Invalid JSON format \
returned -> '{llm_words}'"'''

            except CallMeError as e:
                output.parameters[parameter] = (
                    f'''"ERROR: {e.context["what"][:30]}"'''
                )

            except Exception as e:
                output.parameters[parameter] = f'''"ERROR: {str(e)[:30]}"'''
