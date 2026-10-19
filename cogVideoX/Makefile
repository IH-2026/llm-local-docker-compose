.PHONY: help install lock test lint format build clean

help:
	@printf '%s\n' \
		'install  Install runtime and development dependencies' \
		'lock     Resolve and write Pipfile.lock' \
		'test     Run the test suite' \
		'lint     Check code with Ruff' \
		'format   Format code with Ruff' \
		'build    Build source and wheel distributions' \
		'clean    Remove generated build artifacts'

install:
	pipenv install --dev

lock:
	pipenv lock

test:
	pipenv run pytest

lint:
	pipenv run ruff check .

format:
	pipenv run ruff check --fix .
	pipenv run ruff format .

build:
	pipenv run python -m build

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache
