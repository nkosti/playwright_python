# UI test automation project

## Description

This project will store the UI automated tests.

### Technical stack

- Python 3.8 based project ( any Python version > 3.5 will work)
- Playwright as our UI Web Automation Tool
- Pytest as our Test Runner
- Pytest-BDD as our helper for having a clean BDD suite
- Poetry as a dependency / configuration manager

## How to run the project?

In order to run the project, we'll need to perform the following steps:

## Setting up the local environment and dependencies

Since our project uses Poetry as a dependency / config manager, we'll need to set it up accordingly.

First, let's check which python version do we have **installed** and binded as the default one:

```shell
python --version # Should output Python 3.x.y
```

If the python version is not 3.x.y, we might need either:

- Check if Python3 is installed ( running python3 in the terminal will be enough )
- Install Python3

```shell
python -m pip install poetry
python -m poetry config virtualenvs.in-project true
python -m poetry shell
python -m poetry install
python -m poetry run playwright

# If the command above triggers there are some missing binaries, execute the following one:
poetry run playwright install
```

## Running the tests

### Running all the tests

````shell
python -m poetry run pytest
````

### Running tests in parallel

````shell
python -m poetry run pytest -n $number_of_threads
````

### Running tests of a specific tag or including an specific text in its definition ( either Scenario name or Tags)

````shell
python -m poetry run pytest -k f1-test 
````

### Running tests of a specific tag or subset in parallel

````shell
python -m poetry run pytest -n $number_of_threads -k regression
````

## Environment Support

This project will support execution on multiple environments contains configured in files located at
test/domains/config/environments:

- Dev
- Test
- Integrated

#### Running against a specified environment

By default, if no environment is specified, the target env will be the test one.

In order to specify a environment, we'll need to run the script using the "ENV_NAME" environment variable:

**In UNIX Systems:**

````shell
ENV_NAME=dev python -m poetry run pytest
````

**In Windows Systems:**

```shell
set ENV_NAME=dev
python -m poetry run pytest
```

## Report Support

### Generate Cucumber.json-like report

````shell
python -m poetry run pytest --cucumber-json cucumber.json
````

### Execute tests and generate an Allure Report

````shell
python -m poetry run pytest --alluredir allure-dir
````

### Open Allure Report

````shell
allure serve allure-dir
````