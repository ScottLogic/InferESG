import logging
from typing import Optional
from dataclasses import dataclass
import redis

from src.utils import Config
from src.llm import LLM
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()

redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)


@dataclass
class LLMFile:
    file_name: str
    file_path: Optional[str] = None  # Materiality docs will be local
    file_stream: Optional[bytes] = None  # report agent file will be a stream. Not sure bytes is correct, whatever api/app.py is working with


class OpenAI(LLM):
    client = AsyncOpenAI(api_key=config.openai_key)

    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug(
            "##### Called open ai chat ... llm. Waiting on response model with prompt {0}.".format(
                str([system_prompt, user_prompt])
            )
        )
        try:
            response = await self.client.chat.completions.create(
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

    async def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        files: list[LLMFile]
    ) -> str:
        file_ids = []
        for file in files:
            file_id = redis_client.get(file.file_name)
            if not file_id:
                if file.file_path:
                    file_id = await self.__upload_file(file.file_path)
                elif file.file_stream:
                    file_id = await self.__upload_stream(file.file_stream)
                else:
                    raise ValueError("LLM must have either file_path or file_stream")
            else:
                logger.info(f"found cached file id for {file.file_name}: {file_id}")
            file_ids.append(file_id)

        file_assistant = await self.client.beta.assistants.create(
            name="ESG Analyst",
            instructions=system_prompt,
            model=model,
            tools=[{"type": "file_search"}],
        )

        thread = await self.client.beta.threads.create(
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

        messages = await self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=file_assistant.id
        )

        logger.info(messages.data[0])
        return messages.data[0]  # haven't gotten around to checking how to get the content out yet.

    async def __upload_file(self, file_path: str) -> str:
        file = await self.client.files.create(file=open(file_path, "rb"), purpose="assistants")
        return file.id

    async def __upload_stream(self, file_stream: bytes) -> str:
        file = await self.client.files.create(file=file_stream, purpose="assistants")
        return file.id
