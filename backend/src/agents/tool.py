from typing import Callable, Coroutine, Any
from dataclasses import dataclass


@dataclass
class Parameter:
    type: str
    description: str
    required: bool = True


class CommonParameters:
    USER_QUESTION = {
        "user_question": Parameter("string", "The full question asked by the user.")
    }


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
    parameters: dict[str, Parameter]


def tool(
    name: str,
    description: str,
    parameters: dict[str, Parameter]
) -> Callable[[ToolAction], Tool]:
    def create_tool_from(action: ToolAction) -> Tool:
        return Tool(name, description, action, parameters)

    return create_tool_from
