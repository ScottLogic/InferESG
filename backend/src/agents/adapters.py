from typing import List, Any
from src.agents.tool import Tool
import logging

logger = logging.getLogger(__name__)


def extract_tool(tool_name: str, agent_tools: List[Tool], parameters: dict[str, Any]) -> Tool:
    tool = next((tool for tool in agent_tools if tool.name == tool_name), None)
    if not tool:
        raise Exception(f"Unable to find tool \"{tool_name}\" in available tools")
    validate_args(tool, parameters)
    return tool


def validate_args(tool: Tool, parameters: dict[str, Any]):
    all_params = set(tool.parameters.keys())
    required_params = {key for key, param in tool.parameters.items() if param.required}
    input_params = set(parameters.keys())

    unknown_parameters = input_params - all_params
    missing_parameters = required_params - input_params

    if missing_parameters or unknown_parameters:
        raise Exception(
            f"Tool {tool.name} has parameters {all_params}. Tool was called with {input_params}. "
            f"Missing Parameters: {missing_parameters}. Unknown Parameters: {unknown_parameters}."
        )
