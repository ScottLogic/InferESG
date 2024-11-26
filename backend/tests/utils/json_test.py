import pytest
from src.utils.json import try_pretty_print
from src.utils import to_json


def test_to_json_success():
    input = '{"key": "value"}'

    assert to_json(input) == {"key": "value"}


def test_to_json_failure():
    input = "invalid"

    with pytest.raises(Exception) as error:
        to_json(input)

    assert str(error.value) == f'Failed to interpret JSON: "{input}"'

def test_try_pretty_print():
    obj = {"key": "value", "error": Exception("some error")}
    output = try_pretty_print(obj)

    assert output == '{\n    "key": "value",\n    "error": "Exception: some error"\n}'
