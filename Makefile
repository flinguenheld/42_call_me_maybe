NAME="call_me_maybe.py"
# CACHE_GOINFRE=--cache-dir "~/goinfre/.cache_call_me/"
CACHE_GOINFRE=

install:
	uv $(CACHE_GOINFRE) sync

run:
	uv $(CACHE_GOINFRE) run python -m $(NAME)

helix:
	uv $(CACHE_GOINFRE) run hx .

debug:
	uv $(CACHE_GOINFRE) run python -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calls.json

clean:
	uv $(CACHE_GOINFRE) cache clean
	rm -rf __pycache__ .mypy_cache .venv uv.lock

lint:
	uv $(CACHE_GOINFRE) run flake8 . --extend-exclude \
			'.venv/,llm_sdk/,.cache_call_me'
	uv $(CACHE_GOINFRE) run mypy . --warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs \
			--exclude 'llm_sdk/' \
			--exclude '.cache_call_me/'

lint-strict:
	- uv $(CACHE_GOINFRE) run flake8 . --extend-exclude '.venv,llm_sdk/'
	- uv $(CACHE_GOINFRE) run mypy . --strict --exclude 'llm_sdk/'
