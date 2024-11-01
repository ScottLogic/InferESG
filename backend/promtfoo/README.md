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
Promptfoo configuration (e.g. LLM model) can be set in `promptfooconfig.yaml`

* Use `promptfoo eval` to run all promptfoo tests.
* Use `promptfoo eval -c generate_message_suggestions_config.yaml` to run a specific test suite.
* Use `promptfoo view` to view the results in browser.
