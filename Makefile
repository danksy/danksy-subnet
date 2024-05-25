.PHONY: setup test lint clean

setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

test:
	@./venv/bin/pytest

lint:
	./venv/bin/flake8 myproject

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
