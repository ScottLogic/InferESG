import pytest

from src.agents.esg_report_agent import ESGReportAgent
from src.llm.factory import get_llm

mock_model = "mockmodel"
mock_llm = get_llm("mockllm")

@pytest.mark.asyncio
async def test_invoke_calls_llm(mocker):
    esg_agent = ESGReportAgent(llm_name="mockllm", model=mock_model)
    mock_response = "A Test Report"

    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    response = await esg_agent.invoke("Test Document")

    assert response == mock_response

