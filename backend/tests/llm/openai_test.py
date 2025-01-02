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
class MockFileResponse:
    id: str
    filename: str


@dataclass
class MockMessage:
    content: list[TextContentBlock]


class MockListResponse:
    data = [
        MockMessage(
            content=[
                TextContentBlock(
                    text=Text(
                        annotations=[
                            FileCitationAnnotation(
                                file_citation=FileCitation(file_id="123"),
                                text="【7†source】",
                                end_index=1,
                                start_index=2,
                                type="file_citation",
                            ),
                            FileCitationAnnotation(
                                file_citation=FileCitation(file_id="123"),
                                text="【1:9†source】",
                                end_index=1,
                                start_index=2,
                                type="file_citation",
                            ),
                        ],
                        value="Response with quote【7†source】【1:9†source】",
                    ),
                    type="text",
                )
            ]
        )
    ]


@pytest.mark.asyncio
@patch("src.llm.openai.AsyncOpenAI")
@patch("src.llm.openai.OpenAILLMFileUploadManager.upload_files")
async def test_chat_with_file_removes_citations(upload_files_method, mock_async_openai):
    upload_files_method.return_value = AsyncMock(return_value=["file_id_1"])

    mock_instance = mock_async_openai.return_value

    mock_instance.beta.assistants.create = AsyncMock(return_value=MockResponse(id="assistant-id"))
    mock_instance.beta.threads.create = AsyncMock(return_value=MockResponse(id="thread-id"))
    mock_instance.beta.threads.runs.create_and_poll = AsyncMock(return_value=MockResponse(id="run-id"))
    mock_instance.beta.threads.messages.list = AsyncMock(return_value=MockListResponse())

    client = OpenAI()
    response = await client.chat_with_file(
        model="",
        user_prompt="",
        system_prompt="",
        files=[LLMFile("filename", Path("./backend/library/AstraZeneca-Sustainability-Report-2023.pdf"))],
    )
    assert response == "Response with quote"
