from typing import Callable, Coroutine, Any, Optional
from dataclasses import dataclass


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
class Tool:
    name: str
    description: str
    action: ToolAction
    parameters: Optional[dict[str, Parameter]] = None


def tool(
    name: str,
    description: str,
    requires_user_question: Optional[bool] = False,
    parameters: Optional[dict[str, Parameter]] = None
) -> Callable[[ToolAction], Tool]:
    if not parameters:
        parameters = {}

    def create_tool_from(action: ToolAction) -> Tool:
        if requires_user_question:
            parameters["user_question"] = Parameter(type="string", description="The full question asked by the user.")
        return Tool(name, description, action, parameters)

    return create_tool_from
