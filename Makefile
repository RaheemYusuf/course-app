.PHONY: run install clean check runner
>DEFAULT_GOAL:= runner

run:
	cd src; poetry run python runner.py;

install: pyproject.toml
	poetry install --no-root

clean:
	rm -rf `find . -type d -name __pycache__`

check:
	poetry run flake8 src

runner: check run clean