import pytest
from src.llm.factory import get_llm
from tests.llm.mock_llm import MockLLM
from src.llm.llm import LLMFileFromBytes
from src.agents.report_agent import ReportAgent

mock_model = "mockmodel"
MockLLM()
mock_llm = get_llm("mockllm")

@pytest.mark.asyncio
async def test_invoke_calls_llm(mocker):
    report_agent = ReportAgent(llm_name="mockllm", model=mock_model)
    mock_response = "mocked response"

    mock_file_name = "example_file.txt"
    mock_file_stream = b"This is a mock byte stream."
    mock_file = LLMFileFromBytes(file_name=mock_file_name, file_stream=mock_file_stream)

    mock_llm.chat = mocker.AsyncMock(return_value=mock_response)

    response = await report_agent.create_report(mock_file)

    assert response == mock_response

