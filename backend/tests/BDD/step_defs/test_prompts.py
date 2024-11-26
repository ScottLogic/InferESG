from pytest_bdd import given, when, then, parsers, scenarios
import pytest
import logging
from tests.BDD.test_utilities import (
    send_prompt,
    app_healthcheck,
    correctness_evaluator,
    healthy_response,
    check_response_confidence,
)
from decimal import Decimal
import decimal

logger = logging.getLogger(__name__)

scenarios("../features/Correctness/Accuracy_Factual_Correctness.feature")


@pytest.fixture
def context():
    return {}


@given(parsers.parse("a prompt to InferESG"))
def prepare_prompt(context):
    healthcheck_response = app_healthcheck()
    assert healthcheck_response.status_code == 200
    assert healthcheck_response.json() == healthy_response
    context["health_check_passed"] = True


@when(parsers.parse("I get the response"))
def get_response(context):
    assert context.get("health_check_passed", False)


@then(parsers.parse("the response to this '{prompt}' should match the '{expected_response}'"))
def check_response_includes_expected_response(context, prompt, expected_response):
    response = send_prompt(prompt)
    actual_response = response.json()["answer"]

    # Allow `expected_response` to be a list of possible valid responses
    possible_responses = [resp.strip() for resp in expected_response.split(",")]

    match_found = False
    for expected_resp in possible_responses:
        try:
            expected_value = Decimal(expected_resp)
            actual_value = Decimal(str(actual_response).strip())

            tolerance = Decimal("0.01")
            if abs(expected_value - actual_value) <= tolerance:
                match_found = True
                break  # Exit loop if a match is found

        except (ValueError, decimal.InvalidOperation):
            if expected_resp in str(actual_response).strip():
                match_found = True
                break

    if not match_found:
        # Fallback to the correctness evaluator if none of the options matched
        result = correctness_evaluator.evaluate_strings(
            input=prompt,
            prediction=expected_response,
            reference=actual_response,
        )

        if result["value"] == "N":
            logger.error(
                f"\nTest failed!\n"
                f"Expected one of: {possible_responses}\n"
                f"Actual: {actual_response}\n"
                f"Reasoning: {result.get('reasoning', 'No reasoning provided')}"
            )

        assert result["value"] == "Y", (
            f"\nTest failed!\n"
            f"Expected one of: {possible_responses}\n"
            f"Actual: {actual_response}\n"
            f"Reasoning: {result.get('reasoning', 'No reasoning provided')}"
        )


@then(parsers.parse("the response to this '{prompt}' should give a confident answer"))
def check_bot_response_confidence(prompt):
    response = send_prompt(prompt)
    result = check_response_confidence(prompt, response.json()["answer"])
    assert result["score"] == 1, "The bot response is not confident enough. \nReasoning: " + result["reasoning"]
