from src.agents import ChatAgent, chat_agent, utterance_tool, parameterised_tool, Parameter
from src.agents.tool import ToolActionSuccess, ToolActionFailure, ToolAnswerType
from tests.llm.mock_llm import MockLLM

description = "A test tool"
param_description = "A string"
MockLLM()  # initialise MockLLM so future calls to get_llm will return this object

mock_tool_a_name = "Mock Parameterised Tool A"
mock_tool_b_name = "Mock Parameterised Tool B"
mock_tool_failure_name = "Mock Parameterised Failure Tool"
mock_utterance_tool_name = "Mock Utterance Tool"


@parameterised_tool(
    name=mock_tool_a_name,
    description="A test tool",
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
        "another_optional": Parameter(type="string", description=param_description, required=False),
    },
)
async def mock_tool_a(input: str, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return ToolActionSuccess(input)


@parameterised_tool(
    name=mock_tool_b_name,
    description="A test tool",
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "optional": Parameter(type="string", description=param_description, required=False),
    },
)
async def mock_tool_b(input: str, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return ToolActionSuccess(input)


@parameterised_tool(
    name=mock_tool_failure_name,
    description="Used for mocking a failure response from the tool",
    parameters={
        "input": Parameter(type="string", description=param_description, required=True),
        "retry": Parameter(type="bool", description="Should retry on failure", required=False),
    },
)
async def mock_tool_failure(input: str, retry: bool, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return ToolActionFailure(input, True) if retry else ToolActionFailure(input)


@utterance_tool(
    name=mock_utterance_tool_name,
    description="Used for mocking a failure response from the tool",
)
async def mock_utterance_tool(utterance: str, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return ToolActionSuccess(utterance)


mock_agent_description = "A test agent"
mock_agent_name = "Mock Agent"
mock_prompt = "You are a bot!"
mock_tools = [mock_tool_a, mock_tool_b, mock_tool_failure, mock_utterance_tool]


@chat_agent(name=mock_agent_name, description=mock_agent_description, tools=mock_tools)
class MockChatAgent(ChatAgent):
    async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
        return True


__all__ = [
    "MockChatAgent",
    "mock_agent_description",
    "mock_agent_name",
    "mock_tools",
    "mock_tool_a",
    "mock_tool_b",
    "mock_tool_failure",
    "mock_utterance_tool",
    "mock_tool_a_name",
    "mock_tool_b_name",
    "mock_tool_failure_name",
    "mock_utterance_tool_name"
]
