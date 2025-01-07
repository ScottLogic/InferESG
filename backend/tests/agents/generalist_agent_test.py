from unittest.mock import AsyncMock, patch

import pytest

from src.agents.agent import ChatAgentSuccess
from src.llm.factory import get_llm
from src.agents.generalist_agent import GeneralistAgent


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")


@pytest.mark.asyncio
@patch('src.agents.base_chat_agent.BaseChatAgent.validate', new_callable=AsyncMock)
async def test_generalist_agent(mock_validate, mocker):
    mock_validate.return_value = True

    mock_llm.chat = mocker.AsyncMock(return_value="Example summary.")

    agent = GeneralistAgent(llm_name="mockllm", model=mock_model)

    result = await agent.invoke("example query")
    assert result == ChatAgentSuccess("GeneralistAgent", "Example summary.")
