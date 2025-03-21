.PHONY: setup run test clean

setup:
	pip install -r requirements.txt

run:
	python3 python_code/main.py

test:
	python3 python_code/tests/run_tests.py

clean:
	rm -rf *.pyc __pycache__
