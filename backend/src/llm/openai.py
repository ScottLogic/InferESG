import asyncio
import logging
import time

from src.utils import Config
from src.llm.llm import LLM, LLMFile, LLMFileUploadManager
from src.session.llm_file_upload import (
    add_llm_file_upload,
    get_llm_file_upload,
    get_all_files
)
from openai import NOT_GIVEN, AsyncOpenAI, OpenAIError
from openai.types.beta.threads import Text, TextContentBlock

logger = logging.getLogger(__name__)
config = Config()


def remove_citations(message: Text):
    value = message.value
    for annotation in message.annotations:
        value = value.replace(annotation.text, "")
    return value


class OpenAI(LLM):
    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug(
            "##### Called open ai chat ... llm. Waiting on response model with prompt {0}.".format(
                str([system_prompt, user_prompt])
            )
        )
        try:
            client = AsyncOpenAI(api_key=config.openai_key)
            response = await client.chat.completions.create(
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

            if not content:
                logger.error("Call to Open API failed: message content is None")
                return "An error occurred while processing the request."

            return content
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")
            return "An error occurred while processing the request."

    async def chat_with_file(
        self, model: str, system_prompt: str, user_prompt: str, files: list[LLMFile], return_json=False
    ) -> str:
        client = AsyncOpenAI(api_key=config.openai_key)
        file_ids = await OpenAILLMFileUploadManager().upload_files(files)

        file_assistant = await client.beta.assistants.create(
            name="ESG Analyst",
            instructions=system_prompt,
            model=model,
            tools=[{"type": "file_search"}],
            response_format={"type": "json_object"} if return_json else NOT_GIVEN,
        )

        thread = await client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                    "attachments": [{"file_id": file_id, "tools": [{"type": "file_search"}]} for file_id in file_ids],
                }
            ]
        )

        run = await client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=file_assistant.id)

        messages = await client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)

        if isinstance(messages.data[0].content[0], TextContentBlock):
            message = remove_citations(messages.data[0].content[0].text)
        else:
            message = messages.data[0].content[0].to_json()

        logger.info(f"OpenAI response: {message}")
        return message


class OpenAILLMFileUploadManager(LLMFileUploadManager):
    async def upload_files(self, files: list[LLMFile]) -> list[str]:
        client = AsyncOpenAI(api_key=config.openai_key)

        file_ids = []
        files_to_upload = []
        start_time = time.time()
        for file in files:
            file_id = get_llm_file_upload(file.filename)
            if not file_id:
                logger.info(f"Open AI: Preparing to upload '{file.filename}'")
                file = (file.filename, file.file) if isinstance(file.file, bytes) else file.file
                files_to_upload.append(client.files.create(file=file, purpose="assistants"))
            else:
                file_ids.append(file_id)
                logger.info(f"Open AI: {file.filename} already uploaded to OpenAI with id '{file_id}'")

        uploaded_files = await asyncio.gather(*files_to_upload)

        for file in uploaded_files:
            add_llm_file_upload(file.id, file.filename)
            file_ids.append(file.id)
            logger.info(f"Open AI: File '{file.filename}' uploaded with id '{file.id}'")

        if uploaded_files:
            logger.info(f"Open AI: Time to upload files {time.time() - start_time}")
        return file_ids

    async def delete_all_files(self):
        try:
            client = AsyncOpenAI(api_key=config.openai_key)
            files = get_all_files()
            logger.info(f"Open AI: deleting files {files}")
            delete_tasks = [client.files.delete(file_id=file["file_id"]) for file in files]
            await asyncio.gather(*delete_tasks)
            logger.info("Open AI: Files deleted")
        except OpenAIError:
            logger.info("OpenAI not configured")
