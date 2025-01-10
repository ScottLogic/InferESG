from abc import ABC
from typing import Callable, Coroutine, Any
from dataclasses import dataclass, field


@dataclass
class Parameter:
    type: str
    description: str
    required: bool = True


ToolAnswerType = str | list[Any] | dict[str, Any]


@dataclass
class ToolActionSuccess:
    answer: ToolAnswerType


@dataclass
class ToolActionFailure:
    reason: str
    retry: bool = False


ToolAction = Callable[..., Coroutine[Any, Any, ToolActionSuccess | ToolActionFailure]]


@dataclass
class Tool(ABC):
    name: str
    description: str
    action: ToolAction


@dataclass
class UtteranceTool(Tool):
    """This class represents tools which require utterance only"""


@dataclass
class ParameterisedTool(Tool):
    parameters: dict[str, Parameter] = field(default_factory=lambda: {})


def utterance_tool(name: str, description: str) -> Callable[[ToolAction], UtteranceTool]:
    def create_tool_from(action: ToolAction) -> UtteranceTool:
        return UtteranceTool(name, description, action)

    return create_tool_from


def parameterised_tool(
    name: str,
    description: str,
    parameters: dict[str, Parameter]
) -> Callable[[ToolAction], ParameterisedTool]:
    def create_tool_from(action: ToolAction) -> ParameterisedTool:
        return ParameterisedTool(name, description, action, parameters)

    return create_tool_from
