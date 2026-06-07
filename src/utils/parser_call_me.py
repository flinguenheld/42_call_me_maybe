import argparse
from typing import Dict


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░█▀▄░█▀▀░█▀▀░░░█▀▀░█▀█░█░░░█░░░░░█▄█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀█░█▀▄░▀▀█░█▀▀░░░█░░░█▀█░█░░░█░░░░░█░█░█▀▀░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀░▀░▀▀▀░░
def parse_call_me() -> Dict[str, str]:
    parser = argparse.ArgumentParser(
        prog="Call me maybe",
        description="""Does LLMs speak the language of computers? \
We’ll find out.""",
        usage="uv run python -m src [OPTIONS]",
    )

    parser.add_argument(
        "--functions_definition",
        help="Path to the list function definitions file",
        type=str,
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        help="Path to the list of prompts file",
        type=str,
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        help="Path of the generated output",
        type=str,
        default="data_advanced/output/function_calls.json",
    )
    parser.add_argument(
        "--model",
        help="Model to use (default: qwen)",
        choices=["deepseek", "lama", "qwen"],
        default="qwen",
    )

    args = parser.parse_args()
    return {
        "definitions": args.functions_definition,
        "input": args.input,
        "output": args.output,
        "model": args.model,
    }
