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
    actual_response = response.json()

    try:
        expected_value = Decimal(str(expected_response).strip())
        actual_value = Decimal(str(actual_response).strip())

        tolerance = Decimal("0.01")
        is_equal = abs(expected_value - actual_value) <= tolerance

        if not is_equal:
            pytest.fail(f"\nNumeric values don't match!\n" f"Expected: {expected_value}\n" f"Actual: {actual_value}")

    except (ValueError, decimal.InvalidOperation):
        expected_str = str(expected_response).strip()
        actual_str = str(actual_response).strip()

        logger.info(f"Expected : {expected_str} \nActual: {actual_str}")

        if actual_str.find(expected_str) == -1:
            result = correctness_evaluator.evaluate_strings(
                input=prompt,
                prediction=expected_str,
                reference=actual_str,
            )

            if result["value"] == "N":
                logger.error(
                    f"\nTest failed!\n"
                    f"Expected: {expected_str}\n"
                    f"Actual: {actual_str}\n"
                    f"Reasoning: {result.get('reasoning', 'No reasoning provided')}"
                )

            assert result["value"] == "Y", (
                f"\nTest failed!\n"
                f"Expected: {expected_str}\n"
                f"Actual: {actual_str}\n"
                f"Reasoning: {result.get('reasoning', 'No reasoning provided')}"
            )


@then(parsers.parse("the response to this '{prompt}' should give a confident answer"))
def check_bot_response_confidence(prompt):
    response = send_prompt(prompt)
    result = check_response_confidence(prompt, response.json())
    assert result["score"] == 1, "The bot response is not confident enough. \nReasoning: " + result["reasoning"]
