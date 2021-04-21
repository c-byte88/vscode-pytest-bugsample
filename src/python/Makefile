help:
	@echo "---------------HELP-----------------"
	@echo "To lint the project type        make lint"
	@echo "To work on modules locally type make dev"
	@echo "To run the unit tests type      make test"
	@echo "To clean your local repo type   make clean"
	@echo "To build the projects type      make build"
	@echo "To deploy to dev/PR type        make deploy"
	@echo "------------------------------------"

lint:
	python -m pip install --quiet --upgrade mypy flake8
	mypy . --ignore-missing-imports --exclude "(tests|setup\.py)$"
	flake8 . 
# --ignore=$(shell cat .flakeignore)

dev:
	python -m pip install --upgrade pip setuptools
	pip install -e ./project

test:
	python -m pip install --quiet --upgrade pytest pytest-cov
	@echo "---------------project_Pipeline Tests-----------------"
	pytest ./project/ -ra --cov=./project/ --cov-report term --cov-config ../../setup.cfg


test-security:
	python -m pip install --quiet --upgrade bandit 
	bandit -r ./project -f screen || true

build: clean
	python -m pip install --quiet --upgrade wheel
	python ./project setup.py bdist_wheel

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ ../junit/ build/ dist/ ../htmlcov/ ../.ipynb_checkpoints/ ../src/notebooks/.ipynb_checkpoints/ .coverage .coverage.xml .noseids
	@find . -not -path './.venv*' -path '*/__pycache__*' -delete
	@find . -not -path './.venv*' -path '*/*.egg-info*' -delete

deploy:
	../deploy.sh
