import pytest

from tests.agents import mock_tool_a, mock_tool_b, mock_tool_a_name
from src.agents.adapters import extract_tool


valid_params = {
    "input": "An example string value for input",
    "optional": "An example optional string value for optional",
    "another_optional": "An example optional string value for another_optional",
}
mock_tools = [mock_tool_a, mock_tool_b]


def test_given_valid_params_then_extract_tool_success():
    assert extract_tool(mock_tool_a_name, mock_tools, valid_params) == mock_tool_a


def test_given_incorrect_tool_then_extract_tool_throws_tool_not_found():
    with pytest.raises(Exception, match="Unable to find tool \"Mock Tool Z\" in available tools"):
        extract_tool("Mock Tool Z", mock_tools, valid_params)


def test_given_empty_tool_name_then_extract_tool_throws_tool_not_found():
    with pytest.raises(Exception, match="Unable to find tool \"\" in available tools"):
        extract_tool("", mock_tools, valid_params)


def test_when_given_parameter_that_does_not_exist_then_extract_tool_throws_invalid_params_exception():
    with pytest.raises(Exception) as exception:
        extract_tool(mock_tool_a_name, mock_tools, {"incorrect_param": "incorrect", **valid_params})
    assert "Unknown Parameters: {'incorrect_param'}." in exception.value.args[0]
    assert "Missing Parameters: set()." in exception.value.args[0]


def test_when_given_input_missing_an_optional_parameter_then_extract_tool_succeeds():
    missing_optional_params = {
        "input": "An example string value for input"
    }
    assert extract_tool(mock_tool_a_name, mock_tools, missing_optional_params) == mock_tool_a


def test_when_given_input_missing_a_required_parameter_then_extract_tool_throws_exception():
    missing_required_params = {
        "optional": "An example optional string value for optional",
        "another_optional": "An example optional string value for another_optional",
    }
    with pytest.raises(Exception) as exception:
        extract_tool(mock_tool_a_name, mock_tools, missing_required_params)
    assert "Unknown Parameters: set()." in exception.value.args[0]
    assert "Missing Parameters: {'input'}." in exception.value.args[0]


def test_when_given_incorrect_parameter_and_missing_required_parameter_then_extract_tool_throws_exception():
    bad_params = {
        "optional": "An example optional string value for optional",
        "incorrect_param": "incorrect"
    }
    with pytest.raises(Exception) as exception:
        extract_tool(mock_tool_a_name, mock_tools, bad_params)
    assert "Unknown Parameters: {'incorrect_param'}." in exception.value.args[0]
    assert "Missing Parameters: {'input'}." in exception.value.args[0]
