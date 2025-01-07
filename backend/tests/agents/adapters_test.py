import pytest
from tests.agents import mock_tool_a, mock_tool_b, mock_tool_a_name
from src.agents.adapters import extract_tool, validate_args


def test_extract_tool_success():
    assert extract_tool(mock_tool_a_name, [mock_tool_a, mock_tool_b]) == mock_tool_a


def test_extract_tool_failure():
    with pytest.raises(Exception, match="Unable to find tool Mock Tool Z in available tools"):
        extract_tool("Mock Tool Z", [mock_tool_a, mock_tool_b])


def test_extract_tool_no_tool_found():
    with pytest.raises(Exception, match="No tool deemed appropriate for task"):
        extract_tool("None", [mock_tool_a, mock_tool_b])


def test_validate_all_args_success():
    valid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
        "another_optional": "An example optional string value for another_optional",
    }
    try:
        validate_args(mock_tool_a, valid_args)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_some_optional_passed_success():
    valid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
    }
    try:
        validate_args(mock_tool_a, valid_args)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_no_optional_passed_success():
    valid_args = {"input": "An example string value for input"}
    try:
        validate_args(mock_tool_a, valid_args)
    except Exception:
        pytest.fail("Error: Valid arguments thrown Exception in validate_args")


def test_validate_args_failure():
    invalid_args = {"argument": "An example string value for argument"}
    with pytest.raises(Exception, match=r"Unable to fit parameters .* to Tool arguments .*: Wrong params"):
        validate_args(mock_tool_a, invalid_args)


def test_validate_extra_args_failure():
    invalid_args = {
        "input": "An example string value for input",
        "optional": "An example optional string value for optional",
        "another_optional": "An example optional string value for another_optional",
        "argument": "An example string value for argument",
    }
    with pytest.raises(Exception, match=r"Unable to fit parameters .* to Tool arguments .*: Extra params"):
        validate_args(mock_tool_a, invalid_args)
