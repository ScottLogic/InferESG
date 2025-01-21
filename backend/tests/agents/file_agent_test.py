
from src.session.file_uploads import FileUploadMeta
from src.agents.file_agent import FileAgent


def test_generate_description(mocker):
    mocker.patch("src.agents.file_agent.get_session_file_uploads_meta", return_value=[FileUploadMeta(
        id="1",
        filename="test.pdf",
        upload_id=None
    )])

    agent = FileAgent("mockllm", "mock_model")

    assert callable(agent.description)
    assert agent.description() == ("This agent can retrieve information from files uploaded into InferESG. "
                                   "The following files have been uploaded test.pdf")
