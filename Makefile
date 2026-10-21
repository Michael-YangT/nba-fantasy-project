PHONY: install run test

install:
	pip install -r requirements.txt

run:
	python run.py

test:
	pytest -q
