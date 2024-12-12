import pytest
from dataclasses import dataclass
from pathlib import Path

from unittest.mock import patch, AsyncMock
from openai.types.beta.threads import Text, FileCitationAnnotation, TextContentBlock
from openai.types.beta.threads.file_citation_annotation import FileCitation

from src.llm import LLMFileFromPath
from src.llm.openai import OpenAI


def mock_openai_object(id_value: str) -> AsyncMock:
    mock_obj = AsyncMock()
    mock_obj.id = id_value
    return AsyncMock(return_value=mock_obj)


@dataclass
class MockMessage:
    content: list[TextContentBlock]


class MockListResponse:
    data = [MockMessage(content=[TextContentBlock(
        text=Text(
            annotations=[
                FileCitationAnnotation(
                    file_citation=FileCitation(file_id="123"),
                    text="【7†source】",
                    end_index=1,
                    start_index=2,
                    type="file_citation"
                ),
                FileCitationAnnotation(
                    file_citation=FileCitation(file_id="123"),
                    text="【1:9†source】",
                    end_index=1,
                    start_index=2,
                    type="file_citation"
                )
            ],
            value="Response with quote【7†source】【1:9†source】"
        ),
        type="text"
    )])]


mock_message_list = {"data"}


@pytest.mark.asyncio
@patch("src.llm.openai.OpenAI.client")
async def test_chat_with_file_removes_citations(mock_client):
    mock_client.files.create = mock_openai_object(id_value="file-id")
    mock_client.beta.assistants.create = mock_openai_object(id_value="assistant-id")
    mock_client.beta.threads.create = mock_openai_object(id_value="thread-id")
    mock_client.beta.threads.runs.create_and_poll = mock_openai_object(id_value="run-id")
    mock_client.beta.threads.messages.list = AsyncMock(return_value=MockListResponse)

    client = OpenAI()
    response = await client.chat_with_file(
        model="",
        user_prompt="",
        system_prompt="",
        files_by_path=[LLMFileFromPath("file_name", Path("file/path"))]
    )
    assert response == "Response with quote"
