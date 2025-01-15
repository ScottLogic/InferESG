import dataclasses
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
from typing import List, Type, TypeVar, Any, Callable

from src.agents.adapters import extract_tool
from src.llm import LLM, get_llm
from src.utils import Config
from src.prompts import PromptEngine
from src.agents.tool import Tool, ToolActionFailure, ToolAnswerType

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

    async def invoke(
        self, utterance: str, tool_name: str, parameters: dict[str, Any]
    ) -> ChatAgentSuccess | ChatAgentFailure:
        name = self.__class__.__name__

        try:
            tool = extract_tool(tool_name, self.tools, parameters)
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

    def get_agent_details(self) -> dict[str, Any]:
        return {
            "agent": self.name,
            "description": self.description() if callable(self.description) else self.description,
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        key: dataclasses.asdict(parameter) for key, parameter in tool.parameters.items()
                    }
                }
                for tool in self.tools
            ]
        }


T = TypeVar('T', bound=ChatAgent)


def chat_agent(name: str, description: str | Callable, tools: List[Tool]):

    def decorator(_chat_agent: Type[T]) -> Type[T]:
        _chat_agent.name = name
        _chat_agent.description = description
        _chat_agent.tools = tools
        return _chat_agent

    return decorator
