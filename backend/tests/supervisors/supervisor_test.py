import pytest

from src.agents.agent import ChatAgentFailure, ChatAgentSuccess
from tests.agents import MockChatAgent
from src.supervisors import (
    solve_questions,
    solve_question,
    no_questions_response,
    unsolvable_response,
    no_agent_response
)

mock_model = "mockmodel"
mock_answer = "answer"
scratchpad = []
task = {"query": "Solve this problem"}
query = "example query"
intent_json = {
    "query": query,
    "user_intent": "example intent",
    "questions": [
        {
            "query": "example query",
            "question_intent": "example intent",
            "operation": "example operation",
            "question_category": "example category",
            "parameters": [{"type": "example type", "value": "example value"}],
            "aggregation": "example aggregation",
            "sort_order": "example sort_order",
            "timeframe": "example timeframe",
        }
    ],
}

chat_agent = MockChatAgent("mockllm", mock_model)


@pytest.mark.asyncio
async def test_solve_all_no_tasks():
    with pytest.raises(Exception) as error:
        await solve_questions([])
        assert error == no_questions_response


@pytest.mark.asyncio
async def test_solve_questions(mocker):
    chat_agent_success_1 = ChatAgentSuccess("MockChatAgent", "mock answer 1")
    chat_agent_success_2 = ChatAgentSuccess("MockChatAgent", "mock answer 2")
    chat_agent.invoke = mocker.AsyncMock(side_effect=[chat_agent_success_1, chat_agent_success_2])
    spy_invoke = mocker.spy(chat_agent, 'invoke')

    patched_get_agent = mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=chat_agent)
    mock_scratchpad = mocker.patch("src.supervisors.supervisor.update_scratchpad")
    await solve_questions(["question1", "question2"])

    assert patched_get_agent.call_count == 2
    assert spy_invoke.call_count == 2
    assert mock_scratchpad.call_count == 2
    assert mock_scratchpad.call_args_list[0] == mocker.call("MockChatAgent", "question1", "mock answer 1")
    assert mock_scratchpad.call_args_list[1] == mocker.call("MockChatAgent", "question2", "mock answer 2")


@pytest.mark.asyncio
async def test_solve_question_when_first_agent_succeeds(mocker):
    expected = ChatAgentSuccess("MockChatAgent", mock_answer)
    chat_agent.invoke = mocker.AsyncMock(return_value=expected)
    spy_invoke = mocker.spy(chat_agent, 'invoke')

    patched_get_agent = mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=chat_agent)
    answer = await solve_question(task, scratchpad)

    assert answer == expected
    assert patched_get_agent.call_count == 1
    assert spy_invoke.call_count == 1


@pytest.mark.asyncio
async def test_solve_question_when_agent_fails_first_attempt_and_succeeds_on_retry(mocker):
    expected = ChatAgentSuccess("MockChatAgent", mock_answer)
    chat_agent.invoke = mocker.AsyncMock(side_effect=[
        ChatAgentFailure("MockChatAgent", "failure", retry=True),
        expected
    ])
    spy_invoke = mocker.spy(chat_agent, 'invoke')

    patched_get_agent = mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=chat_agent)
    answer = await solve_question(task, scratchpad)

    assert answer == expected
    assert patched_get_agent.call_count == 1
    assert spy_invoke.call_count == 2


@pytest.mark.asyncio
async def test_solve_question_when_first_agent_fails_no_retry_and_second_agent_succeeds(mocker):
    expected = ChatAgentSuccess("MockChatAgent2", mock_answer)

    good_agent = MockChatAgent("mockllm", mock_model)
    bad_agent = MockChatAgent("mockllm", mock_model)

    good_agent.invoke = mocker.AsyncMock(return_value=expected)
    bad_agent.invoke = mocker.AsyncMock(return_value=ChatAgentFailure("MockChatAgent", "failure"))

    good_agent_spy_invoke_1 = mocker.spy(good_agent, 'invoke')
    bad_agent_spy_invoke_2 = mocker.spy(bad_agent, 'invoke')

    patched_get_agent = mocker.patch(
        "src.supervisors.supervisor.get_agent_for_task",
        side_effect=[bad_agent, good_agent]
    )
    answer = await solve_question(task, scratchpad)

    assert answer == expected
    assert patched_get_agent.call_count == 2
    assert good_agent_spy_invoke_1.call_count == 1
    assert bad_agent_spy_invoke_2.call_count == 1


@pytest.mark.asyncio
async def test_solve_question_unsolvable(mocker):
    chat_agent.invoke = mocker.MagicMock(return_value=ChatAgentFailure("MockChatAgent", "failure"))
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=chat_agent)

    with pytest.raises(Exception) as error:
        await solve_question(task, scratchpad)
        assert error == unsolvable_response


@pytest.mark.asyncio
async def test_solve_question_no_agent_found(mocker):
    mocker.patch("src.supervisors.supervisor.get_agent_for_task", return_value=None)

    with pytest.raises(Exception) as error:
        await solve_question(task, scratchpad)
        assert error == no_agent_response
