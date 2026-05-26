import argparse
from typing import Dict


def parse_call_me() -> Dict[str, str] | None:
    parser = argparse.ArgumentParser(
        prog="Call me maybe",
        usage="""uv run python -m src \
[--functions_definition <function_definition_file>] \
[--input <input_file>] [-- output <output_file>]""",
        description="""Does LLMs speak the language of computers? \
We’ll find out.""",
    )

    parser.add_argument(
        "--functions_definition",
        help="Function definition file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--input",
        help="Input file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        help="Output file",
        type=str,
        required=True,
    )

    try:
        args = parser.parse_args()
        return {
            "definitions": args.functions_definition,
            "input": args.input,
            "output": args.output,
        }
    except SystemExit:
        return None
