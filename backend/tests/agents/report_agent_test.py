import pytest

from src.agents.report_agent import ReportAgent
from src.llm.factory import get_llm

mock_model = "mockmodel"
mock_llm = get_llm("mockllm")


@pytest.mark.asyncio
async def test_invoke_calls_llm(mocker):
    report_agent = ReportAgent(llm_name="mockllm", model=mock_model)
    mock_response = "A Test Report"

    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    response = await report_agent.create_report("Test Document", materiality_topics={"abc": "123"})

    assert response == mock_response
