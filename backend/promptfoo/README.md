# Promptfoo

Promptfoo is a CLI and library for evaluating and red-teaming LLM apps.

See https://www.promptfoo.dev/docs/intro/

## Setup

### Install Promptfoo
Install promptfoo by running `npx install promptfoo`

### Activate Python venv
Promptfoo must be run in a python virtual environment as python is used to load the jinja prompt templates.
To set up a virtual environment, see [Running Locally](../README.md)

## Run Promptfoo
Promptfoo has no way of fetching the OPENAI_API_KEY from our env file.
You will need to run the follow using the OPENAI_KEY from the `.env` file:
`export OPENAI_API_KEY=<OPENAI_KEY>`

Promptfoo has no way to run all test suites, you must manually list each file you want to run.

* Use `promptfoo eval -c generate_message_suggestions_config.yaml` to run a specific test suite.
* Use `promptfoo view` to view the results in browser.

### Debugging tests

Tests can be debugged using `print("...")` messages and adding the `--verbose` argument when calling promptfoo to run tests.
