import json
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
from typing import Callable, List, Type, TypeVar, Tuple, Any

from src.llm import LLM, get_llm
from src.agents.adapters import create_all_tools_str, extract_tool, validate_args
from src.utils import get_scratchpad, Config
from src.prompts import PromptEngine
from src.agents.tool import Tool, ParameterisedTool, UtteranceTool, ToolActionFailure, ToolAnswerType

logger = logging.getLogger(__name__)
engine = PromptEngine()
config = Config()


class Agent(ABC):
    llm: LLM
    model: str

    def __init__(self, llm_name: str | None, model: str | None):
        self.llm = get_llm(llm_name)
        if model is None:
            raise ValueError("LLM Model Not Provided")
        self.model = model


@dataclass
class ChatAgentSuccess:
    agent_name: str
    answer: ToolAnswerType


@dataclass
class ChatAgentFailure:
    agent_name: str
    reason: str
    retry: bool = False


class ChatAgent(Agent):
    name: str
    description: str | Callable[[], str]
    tools: List[Tool]

    async def __select_tool(self, utterance: str) -> Tuple[Tool, Any]:
        if len(self.tools) == 1 and isinstance(self.tools[0], UtteranceTool):
            return self.tools[0], {"utterance": utterance}

        select_tool_response = json.loads(await self.llm.chat(
            self.model,
            engine.load_prompt("tool-selection-format"),
            engine.load_prompt(
                "best-tool",
                task=utterance,
                scratchpad=get_scratchpad(),
                tools=create_all_tools_str(self.tools),
            ),
            return_json=True
        ))

        tool = extract_tool(select_tool_response["tool_name"], self.tools)
        if isinstance(tool, ParameterisedTool):
            tool_parameters = select_tool_response["tool_parameters"]
            validate_args(tool, tool_parameters)
            return tool, tool_parameters

        return tool, {"utterance": utterance}

    async def invoke(self, utterance: str) -> ChatAgentSuccess | ChatAgentFailure:
        name = self.__class__.__name__
        if len(self.tools) < 1:
            return ChatAgentFailure(name, f"{name} has no tools")

        try:
            (tool, parameters) = await self.__select_tool(utterance)
            logger.info(f"{name} selected tool [{tool.name}] with parameters [{parameters}]")

            result = await tool.action(**parameters, llm=self.llm, model=self.model)
        except Exception as e:
            return ChatAgentFailure(name, f"{name} raised the following exception: {e}")

        if isinstance(result, ToolActionFailure):
            return ChatAgentFailure(name, f"{name} tool failed with: {result.reason}", result.retry)

        if await self.validate(utterance, result.answer):
            return ChatAgentSuccess(name, result.answer)

        return ChatAgentFailure(name, f"{name} failed to create a response that would pass validation", True)

    @abstractmethod
    async def validate(self, utterance: str, answer: ToolAnswerType) -> bool:
        pass


T = TypeVar('T', bound=ChatAgent)


def chat_agent(name: str, description: str | Callable, tools: List[Tool | ParameterisedTool]):

    def decorator(_chat_agent: Type[T]) -> Type[T]:
        _chat_agent.name = name
        _chat_agent.description = description
        _chat_agent.tools = tools
        return _chat_agent

    return decorator
