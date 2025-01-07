from typing import Callable, Coroutine, Any
from dataclasses import dataclass, field


@dataclass
class Parameter:
    type: str
    description: str
    required: bool = True


@dataclass
class ToolActionSuccess:
    content: str


@dataclass
class ToolActionFailure:
    reason: str
    retry: bool = True


ToolAction = Callable[..., Coroutine[Any, Any, ToolActionSuccess | ToolActionFailure]]


@dataclass
class Tool:
    name: str
    description: str
    action: ToolAction


@dataclass
class ParameterisedTool(Tool):
    parameters: dict[str, Parameter] = field(default_factory=lambda: {})


def tool(name: str, description: str) -> Callable[[ToolAction], Tool]:
    def create_tool_from(action: ToolAction) -> Tool:
        return Tool(name, description, action)

    return create_tool_from


def parameterised_tool(
    name: str,
    description: str,
    parameters: dict[str, Parameter]
) -> Callable[[ToolAction], ParameterisedTool]:
    def create_tool_from(action: ToolAction) -> ParameterisedTool:
        return ParameterisedTool(name, description, action, parameters)

    return create_tool_from
