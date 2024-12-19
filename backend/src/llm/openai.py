import logging

from src.utils import Config
from src.llm import LLM, LLMFile
from openai import NOT_GIVEN, AsyncOpenAI
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
                logger.error("Call to Mistral API failed: message content is None")
                return "An error occurred while processing the request."

            return content
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")
            return "An error occurred while processing the request."

    async def chat_with_file(self, model: str, system_prompt: str, user_prompt: str, files: list[LLMFile]) -> str:
        client = AsyncOpenAI(api_key=config.openai_key)
        file_ids = await self.__upload_files(files)

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

    async def __upload_files(self, files: list[LLMFile]) -> list[str]:
        client = AsyncOpenAI(api_key=config.openai_key)

        file_ids = []
        for file in files:
            logger.info(f"Uploading file '{file.file_name}' to OpenAI")
            file = (file.file_name, file.file) if isinstance(file.file, bytes) else file.file
            response = await client.files.create(file=file, purpose="assistants")
            file_ids.append(response.id)

        return file_ids
