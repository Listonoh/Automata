build:
	rm dist/*
	python3 -m build

upgrade:
	python3 -m pip install --upgrade twine

upload:
	python3 -m twine upload dist/*

test:
	black .
	pytest

create_venv: 
	pip -m venv .venv
	activate .venv/activate

install: create_venv
	pip install -r requirements.txt