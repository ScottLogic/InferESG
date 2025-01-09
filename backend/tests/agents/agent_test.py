import json
from typing import Any

import pytest
from pytest import raises

from src.agents.tool import ToolAnswerType
from src.agents.agent import chat_agent, ChatAgent, ChatAgentSuccess, ChatAgentFailure
from tests.agents import (
    MockChatAgent,
    mock_utterance_tool_name,
    mock_tool_a_name,
    mock_tool_failure_name,
    mock_utterance_tool,
    mock_tool_a
)
from src.llm.factory import get_llm


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")
mock_agent_instance = MockChatAgent("mockllm", mock_model)
tool_input = "string for tool to output"


def mock_response(tool_name: str, tool_parameters: dict[str, Any]) -> str:
    return json.dumps({"tool_name": tool_name, "tool_parameters": tool_parameters, "reasoning": "Mock Reasoning"})


@pytest.mark.asyncio
@pytest.mark.parametrize("pass_validation, expected", [
        (True, ChatAgentSuccess("MockChatAgentWithValidation", tool_input)),
        (False, ChatAgentFailure(
            "MockChatAgentWithValidation",
            "MockChatAgentWithValidation failed to create a response that would pass validation",
            True
        ))
    ],
    ids=[
        "When appropriate tool selected, Chat Agent invokes func with params and passes validation then success result",
        "When appropriate tool selected, Chat Agent invokes func with params and fails validation then failure result",
    ]
)
async def test_chat_agent_invoke_tool(
    mocker,
    pass_validation: bool,
    expected,
):
    @chat_agent(name="mock_chat_agent", description="mock_description", tools=[mock_tool_a])
    class MockChatAgentWithValidation(ChatAgent):
        async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
            return pass_validation

    mocked_response = mock_response(mock_tool_a_name, {"input": tool_input})
    mock_llm.chat = mocker.AsyncMock(return_value=str(mocked_response))

    mock_agent_with_validation = MockChatAgentWithValidation("mockllm", mock_model)

    response = await mock_agent_with_validation.invoke("Mock task to solve")

    assert response == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("mocked_response, expected", [
        (
            mock_response("Undefined Tool", {}),
            "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {},"
            " 'reasoning': 'No tool was appropriate for the task'}"
        ),
        (
            mock_response("None", {}),
            "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {},"
            " 'reasoning': 'No tool was appropriate for the task'}"
        )
    ],
    ids=[
        "When no tool selected, Chat Agent will return failure with reason",
        "When undefined tool selected, Chat Agent will return failure with reason",
    ]
)
async def test_chat_agent_tool_selection_failure(
    mocker,
    mocked_response: str,
    expected: str,
):
    mock_llm.chat = mocker.AsyncMock(return_value=str(mocked_response))

    with raises(Exception) as error:
        await mock_agent_instance.invoke("Mock task to solve")

        assert str(error.value) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("mocked_response, expected", [
        (
            mock_response(mock_tool_failure_name, {"input": tool_input}),
            ChatAgentFailure("MockChatAgent", "MockChatAgent failed to create a response that would pass validation")
        ),
        (
            mock_response(mock_tool_failure_name, {"input": tool_input, "retry:": False}),
            ChatAgentFailure(
                "MockChatAgent",
                "MockChatAgent failed to create a response that would pass validation",
                False
            )
        )
    ],
    ids=[
        "When mock failure tool selected, Chat Agent will return failure result with retry option",
        "When mock failure tool selected (no retry), Chat Agent will return failure result with no retry",
    ]
)
async def test_chat_agent_tool_failure(
    mocker,
    mocked_response: str,
    expected: str
):
    mock_llm.chat = mocker.AsyncMock(return_value=str(mocked_response))

    with raises(Exception) as error:
        await mock_agent_instance.invoke("Mock task to solve")

        assert str(error.value) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("tools, mocked_response, expected", [
        ([mock_utterance_tool, mock_tool_a], mock_response(mock_utterance_tool_name, {}), "Mock task to solve"),
        (
            [mock_utterance_tool, mock_tool_a],
            mock_response(mock_tool_a_name, {"input": tool_input}),
            tool_input
        )
    ],
    ids=[
     "When ChatAgent only has one tool of type Tool then tool is selected and passed utterance",
     "When ChatAgent only has one tool of type ParameterisedTool then parameterised tool is selected and params",
    ]
)
async def test_chat_agent_tool_selection(
    mocker,
    tools: list,
    mocked_response: str,
    expected: str,
):
    @chat_agent(name="mock_chat_agent", description="mock_description", tools=tools)
    class MockChatAgentWithTools(ChatAgent):
        async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
            return True

    mock_llm.chat = mocker.AsyncMock(return_value=str(mocked_response))
    mock_chat_agent = MockChatAgentWithTools("mockllm", mock_model)

    response = await mock_chat_agent.invoke("Mock task to solve")

    assert response == ChatAgentSuccess("MockChatAgentWithTools", expected)


@pytest.mark.asyncio
async def test_chat_agent_with_one_tool_of_type_base_tool(mocker):
    @chat_agent(name="mock_chat_agent", description="mock_description", tools=[mock_utterance_tool])
    class MockChatAgentWithTools(ChatAgent):
        async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
            return True

    mock_chat_agent = MockChatAgentWithTools("mockllm", mock_model)

    response = await mock_chat_agent.invoke("input string")

    assert response == ChatAgentSuccess("MockChatAgentWithTools", "input string")
