import pytest
import json

from src.llm.factory import get_llm
from src.agents.generalist_agent import GeneralistAgent


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")


@pytest.mark.asyncio
async def test_generalist_agent(mocker):
    mock_llm.chat = mocker.AsyncMock(return_value="Example summary.")

    agent = GeneralistAgent(llm_name="mockllm", model=mock_model)

    result = await agent.invoke("example query")
    expected_response = {"content": "Example summary.", "ignore_validation": "false"}
    assert json.loads(result) == expected_response
