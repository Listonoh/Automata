build:
	rm dist/*
	python3 -m build

upgrade:
	python3 -m pip install --upgrade twine

upload:
	python3 -m twine upload dist/*