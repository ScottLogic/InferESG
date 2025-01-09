from io import BytesIO
from fastapi import UploadFile, HTTPException
from fastapi.datastructures import Headers
import pytest
import uuid

from src.session.file_uploads import FileUpload
from src.directors.report_director import create_report_from_file


mock_topics = {"topic1": "topic1 description", "topic2": "topic2 description"}
mock_report = "#Report on upload as markdown"
expected_answer = (
    "Your report for test.txt is ready to view.\n\nThe following materiality topics were identified for "
    "CompanyABC:\n\ntopic1\ntopic1 description\n\ntopic2\ntopic2 "
    "description"
)


@pytest.mark.asyncio
async def test_create_report_from_file(mocker):
    file_upload = FileUpload(id="1", filename="test.txt", content="test", upload_id=None)

    mock_id = uuid.uuid4()
    mocker.patch("uuid.uuid4", return_value=mock_id)

    # Mock report agent
    mock_report_agent = mocker.AsyncMock()
    mock_report_agent.get_company_name.return_value = "CompanyABC"
    mock_report_agent.create_report.return_value = mock_report
    mocker.patch("src.directors.report_director.get_report_agent", return_value=mock_report_agent)

    # Mock materiality agent
    mock_materiality_agent = mocker.AsyncMock()
    mock_materiality_agent.list_material_topics_for_company.return_value = mock_topics
    mocker.patch("src.directors.report_director.get_materiality_agent", return_value=mock_materiality_agent)

    session_file = FileUpload(
        id=str(mock_id),
        filename=file_upload["filename"],
        upload_id=None,
        content=None
    )


    mock_update_session_file_uploads = mocker.patch("src.directors.report_director.update_session_file_uploads")
    mock_store_report = mocker.patch("src.directors.report_director.store_report", return_value=file_upload)

    file = UploadFile(
        file=BytesIO(b"test"), size=12, headers=Headers({"content-type": "text/plain"}), filename="test.txt"
    )
    response = await create_report_from_file(file)

    expected_response = {"filename": "test.txt", "id": str(mock_id), "report": mock_report, "answer": expected_answer}

    mock_update_session_file_uploads.assert_called_once_with(session_file)
    mock_store_report.assert_called_once_with(expected_response)

    mock_materiality_agent.list_material_topics_for_company.assert_called_once_with("CompanyABC")

    assert response == expected_response


@pytest.mark.asyncio
async def test_create_report_from_file_throws_when_missing_filename():
    with pytest.raises(HTTPException) as error:
        file = UploadFile(
            file=BytesIO(b"Sample text content"),
            size=12,
            headers=Headers({"content-type": "text/plain"}),
            filename="",
        )
        await create_report_from_file(file)

    assert error.value.status_code == 400
    assert error.value.detail == "Filename missing from file upload"
