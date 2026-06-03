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
    printer: VisualPrinter,
) -> ModelOutput:

    output = ModelOutput.model_construct()
    output.prompt = question
    output.parameters = {}

    printer.up_blah(0, f"## Prompt: '{question}'\n")
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
        printer.up_blah(0, f"# Prompt: '{question}'\n")
        printer.up_blah(1, ">Function found\n")
        printer.up_blah(2, f"```python\n{function.prototype()}\n```\n")

        talker_parameters = TalkerParameter(
            llm=llm,
            question=question,
            printer=printer,
        )

        talker_parameters.get_arguments(function, output, printer)
    # print(output)

    return output
