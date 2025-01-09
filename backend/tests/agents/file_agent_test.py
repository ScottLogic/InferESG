
from src.session.file_uploads import FileUploadMeta
from src.agents.file_agent import FileAgent


def test_generate_description(mocker):
    mocker.patch("src.agents.file_agent.get_session_file_uploads_meta", return_value=[FileUploadMeta(
        id="1",
        filename="test.pdf",
        upload_id=None
    )])

    agent = FileAgent(llm_name="mockllm", model="mock_model")

    assert (callable(agent.description) and agent.description() ==
             "Extract parts of the following files test.pdf")
