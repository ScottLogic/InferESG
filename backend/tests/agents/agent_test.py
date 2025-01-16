import json
from typing import Any

import pytest
from pytest import raises

from src.agents.tool import ToolAnswerType
from src.agents.agent import chat_agent, ChatAgent, ChatAgentSuccess, ChatAgentFailure
from tests.agents import MockChatAgent, mock_tool_a_name, mock_tool_a
from src.llm.factory import get_llm


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")
mock_agent_instance = MockChatAgent("mockllm", mock_model)
tool_input = "string for tool to output"
valid_params = {
    "input": "An example string value for input",
    "optional": "An example optional string value for optional",
    "another_optional": "An example optional string value for another_optional",
}


def mock_response(tool_name: str, tool_parameters: dict[str, Any]) -> str:
    return json.dumps({"tool_name": tool_name, "tool_parameters": tool_parameters, "reasoning": "Mock Reasoning"})


@pytest.mark.asyncio
@pytest.mark.parametrize("pass_validation, expected", [
        (True, ChatAgentSuccess("MockChatAgentWithValidation", valid_params["input"])),
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

    mock_agent_with_validation = MockChatAgentWithValidation("mockllm", mock_model)

    response = await mock_agent_with_validation.invoke("The original question", mock_tool_a_name, valid_params)

    assert response == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name, expected", [
        (
            "Mock Tool 1234",
            ChatAgentFailure("MockChatAgent", "MockChatAgent raised the following exception: Unable to find "
                                              "tool \"Mock Tool 1234\" in available tools")
        ),
        (
            "",
            ChatAgentFailure("MockChatAgent", "MockChatAgent raised the following exception: Unable to find "
                                              "tool \"\" in available tools")
        )
    ],
    ids=[
        "When incorrect tool select then Chat Agent will return failure with reason",
        "When \"\" tool selected then Chat Agent will return failure with reason",
    ]
)
async def test_chat_agent_tool_selection_failure(
    mocker,
    tool_name: str,
    expected: str,
):
    result = await mock_agent_instance.invoke("Mock task to solve", tool_name, valid_params)
    assert result == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("input_params, expected", [
        (
            {"input": tool_input},
            ChatAgentFailure("MockChatAgent", "MockChatAgent failed to create a response that would pass validation")
        ),
        (
            {"input": tool_input, "retry:": False},
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
    input_params: dict[str, str],
    expected: str
):
    with raises(Exception) as error:
        await mock_agent_instance.invoke("Mock task to solve", mock_tool_a_name, input_params)

        assert str(error.value) == expected
