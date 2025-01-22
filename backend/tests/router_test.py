import json
from unittest.mock import MagicMock

import pytest

from src.agents.agent import ChatAgentFailure
from tests.agents import MockChatAgent, mock_tool_a_name
from tests.llm.mock_llm import MockLLM
from src.router import select_tool_for_question


mock_model = "mockmodel"
mock_llm = MockLLM()
mock_agent_1 = MockChatAgent("mockllm", mock_model)
mock_agent_2 = MockChatAgent("mockllm", mock_model)
mock_agent_2.name = "mock_agent_2"
mock_agents = [mock_agent_1, mock_agent_2]


@pytest.mark.asyncio
async def test_select_agent_for_task_no_agent_found(mocker):
    selected_agent = '{"agent": "this_agent_does_not_exist", "tool": "example_tool", "parameters": {}}'
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=selected_agent)

    agent, tool, parameters = await select_tool_for_question("task1", [])

    assert agent is None


@pytest.mark.asyncio
async def test_select_agent_for_task_agent_found(mocker):
    selected_agent_and_tool = {"agent": mock_agent_1.name, "tool": mock_tool_a_name, "parameters": {"input": "input"}}
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(selected_agent_and_tool))

    agent, tool, parameters = await select_tool_for_question("task1", [])

    assert agent is mock_agent_1
    assert tool == mock_tool_a_name
    assert parameters == {"input": "input"}


@pytest.mark.asyncio
async def test_select_agent_for_task_given_agent_failed_only_once_then_selects_this_agent(mocker):
    plan = {"agent": mock_agent_2.name, "tool": mock_tool_a_name, "parameters": {"input": "input"}}
    chat_agent_failure_1 = ChatAgentFailure(mock_agent_1.name, "failure")
    chat_agent_failure_2 = ChatAgentFailure(mock_agent_2.name, "failure")
    chat_agent_failures = [chat_agent_failure_1, chat_agent_failure_1, chat_agent_failure_2]
    mocker.patch("src.router.get_llm", return_value=mock_llm)
    mocker.patch("src.router.get_chat_agents", return_value=mock_agents)
    mocker.patch("src.router.config.router_model", new_callable=MagicMock)
    mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(plan))
    spy_chat = mocker.spy(mock_llm, 'chat')

    agent, tool, parameters = await select_tool_for_question("task1", chat_agent_failures)

    spy_chat_user_prompt_args = spy_chat.call_args_list[0][0][2]

    assert agent is mock_agent_2
    assert "ChatAgentFailure(agent_name='Mock Agent', reason='failure'" not in spy_chat_user_prompt_args
    assert "ChatAgentFailure(agent_name='mock_agent_2', reason='failure'" in spy_chat_user_prompt_args
    assert "[{'agent': 'mock_agent_2', 'description': 'A test agent'" in spy_chat_user_prompt_args
