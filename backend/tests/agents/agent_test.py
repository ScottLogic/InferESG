import json

import pytest
from pytest import raises
from tests.agents import MockChatAgent
from src.llm.factory import get_llm


mock_model = "mockmodel"
mock_llm = get_llm("mockllm")
mock_agent_instance = MockChatAgent("mockllm", mock_model)


def mock_response(tool_name: str, tool_parameters: dict[str,str]) -> str:
    return json.dumps({"tool_name": tool_name, "tool_parameters": tool_parameters, "reasoning": "Mock Reasoning"})


@pytest.mark.asyncio
@pytest.mark.parametrize("mocked_response, expect_success, expected", [
        (
            mock_response("Mock Tool A", {"input": "string for tool to output"}),
            True,
            "string for tool to output"
        ),
        (
            mock_response("Undefined Tool", {}),
            False,
            "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {},"
            " 'reasoning': 'No tool was appropriate for the task'}"
        ),
        (
            mock_response("None", {}),
            False,
            "Unable to extract chosen tool and parameters from {'tool_name': 'None', 'tool_parameters': {},"
            " 'reasoning': 'No tool was appropriate for the task'}"
        )
    ],
    ids=[
        "When appropriate tool selected, Test Chat Agent invoke func will call tool with parameters",
        "When 'Undefined Tool' selected, Test Chat Agent invoke func will explain no tool was appropriate for task",
        "When 'None' selected, Test Chat Agent invoke func will explain no tool was appropriate for task"
    ]
)
async def test_chat_agent_invoke_uses_tool(mocker, mocked_response: str, expect_success: bool, expected: str):
    mock_llm.chat = mocker.AsyncMock(return_value=str(mocked_response))

    if expect_success:
        response = await mock_agent_instance.invoke("Mock task to solve")

        assert response == expected
    else:
        with raises(Exception) as error:
            await mock_agent_instance.invoke("Mock task to solve")

            assert str(error.value) == expected
