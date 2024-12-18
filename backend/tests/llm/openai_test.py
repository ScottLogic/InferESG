import pytest
from dataclasses import dataclass
from pathlib import Path

from unittest.mock import patch, AsyncMock
from openai.types.beta.threads import Text, FileCitationAnnotation, TextContentBlock
from openai.types.beta.threads.file_citation_annotation import FileCitation

from src.llm import LLMFile
from src.llm.openai import OpenAI


@dataclass
class MockResponse:
    id: str


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
@patch("src.llm.openai.AsyncOpenAI")
async def test_chat_with_file_removes_citations(mock_async_openai):
    mock_instance = mock_async_openai.return_value

    mock_instance.files.create = AsyncMock(return_value=MockResponse(id="file-id"))
    mock_instance.beta.assistants.create = AsyncMock(return_value=MockResponse(id="assistant-id"))
    mock_instance.beta.threads.create = AsyncMock(return_value=MockResponse(id="thread-id"))
    mock_instance.beta.threads.runs.create_and_poll = AsyncMock(return_value=MockResponse(id="run-id"))
    mock_instance.beta.threads.messages.list = AsyncMock(return_value=MockListResponse)

    client = OpenAI()
    response = await client .chat_with_file(
        model="",
        user_prompt="",
        system_prompt="",
        files=[LLMFile("file_name", Path("file/path"))]
    )
    assert response == "Response with quote"
