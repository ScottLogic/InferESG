import json
from unittest.mock import MagicMock

import pytest
from tests.llm.mock_llm import MockLLM
from src.agents.agent import chat_agent, ChatAgent
from src.router import get_agent_for_task


mock_model = "mockmodel"
mock_llm = MockLLM()


class MockChatAgent(ChatAgent):
    async def validate(self, utterance: str, answer: str) -> bool:
        pass


mock_agent_1 = chat_agent("chat_agent_1", "description_1", [])(MockChatAgent("mockllm", mock_model))
mock_agent_2 = chat_agent("chat_agent_2", "description_2", [])(MockChatAgent("mockllm", mock_model))
mock_agents = [mock_agent_1, mock_agent_2]


@pytest.mark.asyncio
async def test_get_agent_for_task_no_agent_found(mocker):
    selected_agent = '{"agent_name": "this_agent_does_not_exist"}'
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=selected_agent)

    agent = await get_agent_for_task("task1", [])

    assert agent is None


@pytest.mark.asyncio
async def test_get_agent_for_task_agent_found(mocker):
    selected_agent = {"agent_name": mock_agent_1.name}
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(selected_agent))

    agent = await get_agent_for_task("task1", [])

    assert agent is mock_agent_1


@pytest.mark.asyncio
async def test_get_agent_for_task_is_not_given_excluded_agents(mocker):
    plan = {"agent_name": mock_agent_2.name}
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(plan))
    spy_chat = mocker.spy(mock_llm, 'chat')

    agent = await get_agent_for_task("task1", [], [mock_agent_1.name])

    assert agent is mock_agent_2
    assert mock_agent_1.name not in spy_chat.call_args_list[0][0][1]
    assert mock_agent_2.name in spy_chat.call_args_list[0][0][1]
