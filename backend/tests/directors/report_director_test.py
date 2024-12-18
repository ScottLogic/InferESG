from io import BytesIO
from fastapi import UploadFile
from fastapi.datastructures import Headers
import pytest

from src.session.file_uploads import FileUpload
from src.directors.report_director import report_on_file_upload


mock_topics = {"topic1": "topic1 description", "topic2": "topic2 description"}
mock_report = "#Report on upload as markdown"
expected_answer = ('Your report for test.txt is ready to view.\n\nThe following materiality topics were identified for '
                   'CompanyABC which the report focuses on:\n\ntopic1\ntopic1 description\n\ntopic2\ntopic2 '
                   'description\n')


@pytest.mark.asyncio
async def test_report_on_file_upload(mocker):
    file_upload = FileUpload(uploadId="1", filename="test.txt", content="test", contentType="text/plain", size=4)

    mock_report_agent = mocker.AsyncMock()
    mock_report_agent.get_company_name.return_value = "CompanyABC"
    mock_report_agent.create_report.return_value = mock_report
    mocker.patch("src.directors.report_director.get_report_agent", return_value=mock_report_agent)
    mock_handle_file_upload = mocker.patch("src.directors.report_director.handle_file_upload", return_value=file_upload)
    mock_store_report = mocker.patch("src.directors.report_director.store_report", return_value=file_upload)

    mock_materiality_agent = mocker.AsyncMock()
    mock_materiality_agent.list_material_topics.return_value = mock_topics
    mocker.patch("src.directors.report_director.get_materiality_agent", return_value=mock_materiality_agent)

    request_upload_file = UploadFile(
        file=BytesIO(b"test"),
        size=12,
        headers=Headers({"content-type": "text/plain"}),
        filename="test.txt"
    )
    response = await report_on_file_upload(request_upload_file)

    expected_response = {"filename": "test.txt", "id": "1", "report": mock_report, "answer": expected_answer}

    mock_report_agent.get_company_name.assert_called_once_with("test")
    mock_handle_file_upload.assert_called_once_with(request_upload_file)
    mock_store_report.assert_called_once_with(expected_response)

    mock_materiality_agent.list_material_topics.assert_called_once_with("CompanyABC")

    assert response == expected_response
