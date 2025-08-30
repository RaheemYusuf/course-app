.PHONY: run install clean check runner
>DEFAULT_GOAL:= runner

run: install
	cd app; poetry run python run.py;

install: pyproject.toml
	poetry install --no-root

clean:
	rm -rf `find . -type d -name __pycache__`

check:
	poetry run flake8 app/

runner: check run clean