# src/llm/openai_llm.py
import logging
from typing import Optional
from dataclasses import dataclass

from src.utils import Config
from src.llm import LLM, LLMChatWithFile
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()


@dataclass
class LLMFile:
    file_name: str
    file_path: Optional[str] = None  # Materiality docs will be local
    file_stream: Optional[bytes] = None  # report agent file will be a stream. Not sure bytes is correct, whatever api/app.py is working with


class OpenAI(LLM):
    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug(
            "##### Called open ai chat ... llm. Waiting on response model with prompt {0}.".format(
                str([system_prompt, user_prompt])
            )
        )
        client = AsyncOpenAI(api_key=config.openai_key)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                response_format={
                    "type": "json_object"} if return_json else NOT_GIVEN,
            )
            content = response.choices[0].message.content
            logger.info(f"OpenAI response: Finish reason: {response.choices[0].finish_reason}, Content: {content}")
            logger.debug(f"Token data: {response.usage}")

            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(content)
            else:
                return "Unexpected content format"
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")
            return "An error occurred while processing the request."


class OpenAIChatWithFile(LLMChatWithFile):
    async def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        files: list[LLMFile]
    ) -> str:
        client = AsyncOpenAI(api_key=config.openai_key)

        file_ids = []
        for file in files:
            # check in Redis if this file exists
                # if it doesn't exist, upload it and save the file_id
                    # if LLMFile has path to upload use upload_file(file_path)
                    # if LLMFile has stream then upload stream
                # if it does exist then redis will have the file id uploaded to openai. fetch it
            file_ids.append("id from logic in pseudo code above")

        file_assistant = await client.beta.assistants.create(
            name="ESG Analyst",
            instructions=system_prompt,
            model=model,
            tools=[{"type": "file_search"}],
        )

        thread = await client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                    "attachments": [
                        {"file_id": file_id, "tools": [{"type": "file_search"}]}
                        for file_id in file_ids
                    ],
                }
            ]
        )

        messages = await client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=file_assistant.id
        )

        logger.info(messages.data[0])
        return messages.data[0]  # haven't gotten around to checking how to get the content out yet.


async def upload_file(file_path: str) -> str:
    client = AsyncOpenAI(api_key=config.openai_key)
    file = await client.files.create(file=open(file_path, "rb"), purpose="assistants")
    return file.id
