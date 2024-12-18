import pytest
from unittest.mock import patch, AsyncMock
import json
from src.agents.generalist_agent import GeneralistAgent


@pytest.mark.asyncio
@patch("src.agents.generalist_agent.answer_user_question", new_callable=AsyncMock)
async def test_generalist_agent(
    mock_answer_user_question,
):
    mock_answer_user_question.return_value = json.dumps(
        {"status": "success", "response": json.dumps({"is_valid": True, "answer": "Example summary."})}
    )
    generalist_agent = GeneralistAgent("llm", "mock_model")

    result = await generalist_agent.invoke("example query")
    expected_response = {"content": "Example summary.", "ignore_validation": "false"}
    assert json.loads(result) == expected_response


@pytest.mark.asyncio
@patch("src.agents.generalist_agent.answer_user_question", new_callable=AsyncMock)
async def test_generalist_agent_reponse_format_error(
    mock_answer_user_question,
):
    mock_answer_user_question.return_value = json.dumps(
        {"status": "success", "response": json.dumps({"is_valid": True, "answer_wrong_format": "Example summary."})}
    )
    generalist_agent = GeneralistAgent("llm", "mock_model")

    result = await generalist_agent.invoke("example query")

    expected_response = {"content": "Error in answer format.", "ignore_validation": "false"}
    assert json.loads(result) == expected_response
