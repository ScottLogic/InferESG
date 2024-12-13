from src.agents import ChatAgent, chat_agent, tool, Parameter
from tests.llm.mock_llm import MockLLM

name_a = "Mock Tool A"
name_b = "Mock Tool B"
description = "A test tool"
param_description = "A string"
MockLLM()  # initialise MockLLM so future calls to get_llm will return this object


@tool(
    name=name_a,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
        "another_optional": Parameter(type="string", description=param_description, required=False),
    },
)
async def mock_tool_a(input: str, llm, model):
    return input


@tool(
    name=name_b,
    description=description,
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
async def mock_tool_b(input: str, llm, model):
    return input


mock_agent_description = "A test agent"
mock_agent_name = "Mock Agent"
mock_prompt = "You are a bot!"
mock_tools = [mock_tool_a, mock_tool_b]


@chat_agent(name=mock_agent_name, description=mock_agent_description, tools=mock_tools)
class MockChatAgent(ChatAgent):
    pass


__all__ = ["MockChatAgent", "mock_agent_description", "mock_agent_name", "mock_tools", "mock_tool_a", "mock_tool_b"]
