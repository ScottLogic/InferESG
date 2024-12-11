from io import BytesIO
from fastapi import UploadFile
from fastapi.datastructures import Headers
import pytest

from src.llm.llm import LLMFileFromBytes
from src.directors.report_director import report_on_file_upload


mock_report = "#Report on upload as markdown"

@pytest.mark.asyncio
async def test_report_on_file_upload(mocker):

    mock_report_agent = mocker.AsyncMock()
    mock_report_agent.create_report.return_value = mock_report
    mocker.patch("src.directors.report_director.get_report_agent", return_value=mock_report_agent)

    request_upload_file = UploadFile(
        file=BytesIO(b"test"),
        size=12,
        headers=Headers({"content-type": "text/plain"}),
        filename="test.txt"
    )
    response = await report_on_file_upload(request_upload_file)

    mock_file_name = "test.txt"
    mock_file_stream = b"test"
    mock_file = LLMFileFromBytes(file_name=mock_file_name, file_stream=mock_file_stream)

    mock_report_agent.create_report.assert_called_once_with(mock_file)
    assert response == {"filename": "test.txt", "report": mock_report}
