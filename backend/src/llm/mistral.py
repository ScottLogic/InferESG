from fastapi import HTTPException
from mistralai import Mistral as MistralApi, UserMessage, SystemMessage
import logging
from src.utils.file_utils import handle_file_upload
from src.utils import Config
from .llm import LLM, LLMFile

logger = logging.getLogger(__name__)
config = Config()


class Mistral(LLM):
    client = MistralApi(api_key=config.mistral_key)

    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug("Called llm. Waiting on response model with prompt {0}.".format(str([system_prompt, user_prompt])))
        response = await self.client.chat.complete_async(
            model=model,
            messages=[
                SystemMessage(content=system_prompt),
                UserMessage(content=user_prompt),
            ],
            temperature=0,
            response_format={"type": "json_object"} if return_json else None,
        )
        if not response or not response.choices:
            logger.error("Call to Mistral API failed: No valid response or choices received")
            return "An error occurred while processing the request."

        content = response.choices[0].message.content
        if not content:
            logger.error("Call to Mistral API failed: message content is None or Unset")
            return "An error occurred while processing the request."

        logger.debug('{0} response : "{1}"'.format(model, content))
        return content

    async def chat_with_file(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        files: list[LLMFile],
    ) -> str:
        try:
            for file in files:
                file = handle_file_upload(file)
                extracted_content = file["content"]
                user_prompt += f"\n\nDocument:\n{extracted_content}"
            return await self.chat(model, system_prompt, user_prompt)
        except Exception as file_error:
            raise HTTPException(status_code=500, detail=f"Failed to process files: {str(file_error)}") from file_error
