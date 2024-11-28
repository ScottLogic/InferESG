from src.utils.scratchpad import clear_scratchpad, get_scratchpad, update_scratchpad


question = "example question"


def test_scratchpad():
    clear_scratchpad()
    assert get_scratchpad() == []
    update_scratchpad("ExampleAgent", question, "example result")
    assert get_scratchpad() == [
        {"agent_name": "ExampleAgent", "question": "example question", "result": "example result", "error": None}
    ]
    clear_scratchpad()
