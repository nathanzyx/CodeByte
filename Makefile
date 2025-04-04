.PHONY: setup run clean

setup:
	pip install -r requirements.txt

run:
	python3 python_code/main.py

clean:
	rm -rf *.pyc __pycache__
