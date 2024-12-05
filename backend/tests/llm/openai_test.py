# tests/test_openai_llm.py
import pytest
from unittest.mock import MagicMock, patch

from openai.types.chat import ChatCompletion, ParsedChatCompletion

from src.llm.openai import OpenAI
from src.utils import Config

mock_config = MagicMock(spec=Config)
mock_config.openai_model = "gpt-3.5-turbo"
system_prompt = "system_prompt"
user_prompt = "user_prompt"
content_response = "Hello there"
openapi_response = "Hello! How can I assist you today?"


def create_mock_chat_response(content):
    return {"choices": [{"message": {"role": "system", "content": content}}]}


# class MockOpenAI:
#     def chat(self):


# @patch("openai.AsyncOpenAI")
# def test_chat_content_string_returns_string(mock_client):
#     mock_client.chat.completions.create.return_value = create_mock_chat_response(content_response)
#     mocker.patch("openai.ChatCompletion.create", side_effect=MockedCompletion())
#     # mock_class = MockOpenAI()
#
#     # Mock the SampleClass with the MockClass
#     # mocker.patch.object(SampleClass, "__new__", return_value = mock_class)
#     client = OpenAI()
#     response = client.chat("gpt-3.5-turbo", "", "", False)
#     assert response == content_response


# @patch("src.llm.openai_client.openai.ChatCompletion.create")
# def test_chat_content_list_returns_string(mock_create):
#     content_list = ["Hello", "there"]
#     mock_create.return_value = create_mock_chat_response(content_list)
#
#     client = OpenAIClient()
#     response = client.chat(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#     )
#
#     assert " ".join(response) == content_response
#
#
# @patch("src.llm.openai_client.openai.ChatCompletion.create")
# def test_chat_handles_exception(mock_create):
#     mock_create.side_effect = Exception("API error")
#
#     client = OpenAIClient()
#     response = client.chat(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#     )
#
#     assert response == "An error occurred while processing the request."


if __name__ == "__main__":
    pytest.main()
