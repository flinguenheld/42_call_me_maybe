NAME="call_me_maybe.py"

install:
	uv sync

run:
	uv run python -m $(NAME)

debug:
	uv run python -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calls.json

clean:
	uv cache clean
	rm -rf __pycache__ .mypy_cache .venv uv.lock

lint:
	- uv run flake8 . --extend-exclude '.venv,llm_sdk/'
	- uv run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \
			--exclude 'llm_sdk/'

lint-strict:
	- uv run flake8 . --extend-exclude '.venv,llm_sdk/'
	- uv run mypy . --strict --exclude 'llm_sdk/'
