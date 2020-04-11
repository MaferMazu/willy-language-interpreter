

clean-pyc:
   find . -name '*.pyc' -exec rm --force {} +
   find . -name '*.pyo' -exec rm --force {} +
   name '*~' -exec rm --force  {}

clean-build:
    rm --force --recursive build/
    rm --force --recursive dist/
    rm --force --recursive *.egg-info

isort:
    sh -c "isort --skip-glob=.tox --recursive . "

lint:
    flake8 --exclude=.tox

.PHONY: clean-pyc clean-build

run:
    python main.py