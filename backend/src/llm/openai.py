import logging
import re
from typing import Optional
import redis

from src.utils.scratchpad import update_scratchpad
from src.utils import Config
from src.llm import LLM, LLMFileFromPath, LLMFileFromBytes
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()

redis_client = redis.Redis(host=config.redis_host, port=6379, decode_responses=True)


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
                response_format={"type": "json_object"} if return_json else NOT_GIVEN,
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
        files_by_path: Optional[list[LLMFileFromPath]] = None,
        files_by_stream: Optional[list[LLMFileFromBytes]] = None,
    ) -> str:
        file_ids = await self.__upload_files(files_by_path, files_by_stream)

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
                    "attachments": [{"file_id": file_id, "tools": [{"type": "file_search"}]} for file_id in file_ids],
                }
            ]
        )

        update_scratchpad(result=thread)
        run = await self.client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=file_assistant.id)

        messages = await self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)

        logger.info(messages)
        return re.sub("【.*?†source】", "", messages.data[0].content[0].text.value)

    async def __upload_files(
        self, files_by_path: Optional[list[LLMFileFromPath]], files_by_stream: Optional[list[LLMFileFromBytes]]
    ) -> list[str]:
        file_ids = []

        files_by_path = files_by_path if files_by_path is not None else []
        files_by_stream = files_by_stream if files_by_stream is not None else []

        for file in files_by_path + files_by_stream:
            file_id = redis_client.get(file.file_name)
            if not file_id:
                if isinstance(file, LLMFileFromPath):
                    file = await self.client.files.create(file=file.file_path, purpose="assistants")
                else:
                    file = await self.client.files.create(file=(file.file_name, file.file_stream), purpose="assistants")
                file_id = file.id
            file_ids.append(file_id)
        return file_ids
