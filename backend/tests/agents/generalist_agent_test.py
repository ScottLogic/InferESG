from unittest.mock import AsyncMock

import pytest

from src.agents.agent import ChatAgentSuccess
from src.llm.factory import get_llm
from src.agents.generalist_agent import GeneralistAgent


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")


@pytest.mark.asyncio
async def test_generalist_agent(mocker):
    mock_llm.chat = mocker.AsyncMock(return_value="Example summary.")

    mock_validator_agent = mocker.patch('src.agents.generalist_agent.ValidatorAgent')
    mock_validator_instance = mock_validator_agent.return_value
    mock_validator_instance.validate = AsyncMock(return_value="true")

    agent = GeneralistAgent(llm_name="mockllm", model=mock_model)

    result = await agent.generalist_answer("example query")
    assert result == ChatAgentSuccess("GeneralistAgent", "Example summary.")
