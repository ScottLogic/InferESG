import logging
from src.prompts import PromptEngine
from src.agents import Agent
from src.utils.log_publisher import LogPrefix, publish_log_info
import json

logger = logging.getLogger(__name__)
engine = PromptEngine()


class ValidatorAgent(Agent):
    async def validate(self, utterance: str) -> str:
        answer = await self.llm.chat(self.model, engine.load_prompt("validator"), utterance)
        response = json.loads(answer)['response']
        await publish_log_info(LogPrefix.USER, f"Validating: '{utterance}' Answer: '{response}'", __name__)

        return response
