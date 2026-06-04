from src.talker.parameter.parameter_regex import TalkerRegex
from src.talker.parameter.parameter_int import TalkerInt
from src.talker.parameter.parameter_bool import TalkerBool
from json import JSONDecodeError
import json
from src.talker.parameter.parameter_float import TalkerFloat
from typing import List

from src.error.error import CallMeError
from src.models.output import ModelOutput
from src.llm_wrapper.llm_wrapper import LLMWrapper
from src.visual.visual_printer import VisualPrinter
from src.talker.function.function import TalkerFunction
from src.models.function_definition import ModelFunction
from src.talker.parameter.parameter import TalkerParameter


@CallMeError.catch("Manage prompt")
def manage_prompt(
    llm: LLMWrapper,
    question: str,
    function_list: List[ModelFunction],
    output_list: List[ModelOutput],
    printer: VisualPrinter,
) -> ModelOutput:

    output = ModelOutput.model_construct()
    output.prompt = question
    output.parameters = {}

    printer.up_prompt_list(question)
    printer.up_blah(1, ">Search function...\n")
    talker_function = TalkerFunction(
        llm=llm,
        question=question,
        functions=function_list,
        printer=printer,
    )

    talker_function.talk()
    if talker_function.found:
        function = talker_function.found
        output.name = function.name
        printer.up_blah(1, ">Function found\n")
        printer.up_blah(2, f"```python\n{function.prototype()}\n```\n")

        get_arguments(llm, function, output, printer)

        # TODO ADD A CHECK TO SEE IF IT'S OK !!!!!!!!!!!!!!!
        # TODO ADD A CHECK TO SEE IF IT'S OK !!!!!!!!!!!!!!!
        # TODO ADD A CHECK TO SEE IF IT'S OK !!!!!!!!!!!!!!!
        output_list.append(output)
    # print(output)

    return output


@CallMeError.catch("Get arguments")
def get_arguments(
    llm: LLMWrapper,
    function: ModelFunction,
    output: ModelOutput,
    printer: VisualPrinter,
) -> None:

    for parameter, value in function.parameters.items():
        try:
            printer.up_blah(3, f">Search parameter '{parameter}'")

            if parameter.lower() == "regex":
                talker = TalkerRegex(
                    output.prompt, llm, printer, function, parameter
                )
            else:
                match value["type"]:
                    case "number" | "float":
                        talker = TalkerFloat(
                            output.prompt, llm, printer, function, parameter
                        )
                    case "integer" | "int":
                        talker = TalkerInt(
                            output.prompt, llm, printer, function, parameter
                        )
                    case "boolean" | "bool":
                        talker = TalkerBool(
                            output.prompt, llm, printer, function, parameter
                        )
                    case _:
                        talker = TalkerParameter(
                            output.prompt, llm, printer, function, parameter
                        )

            json_arg = json.loads(talker.talk())
            output.parameters[parameter] = json_arg[parameter]

        # TODO: CHANGE THAT TO SET VALUE AS NOT FOUND ?
        except JSONDecodeError as e:
            raise CallMeError(
                blah=str(e),
                prompt=output.prompt,
                what=f"Can't get the parameter '{parameter}'",
                why="The returned JSON format is invalid",
            )

        except Exception as e:
            raise CallMeError(
                what=f"Can't get the parameter '{parameter}'",
                prompt=output.prompt,
                error=str(e),
            )
