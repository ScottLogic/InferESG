from src.prompts import PromptEngine
from src.agents import Agent, agent
import logging
from src.utils.config import Config


config = Config()

engine = PromptEngine()
intent_format = engine.load_prompt("intent-format")
logger = logging.getLogger(__name__)


@agent(
    name="IntentAgent",
    description="This agent is responsible for determining the intent of the user's utterance",
    tools=[],
)
class IntentAgent(Agent):

    async def invoke(self, utterance: str) -> str:
        chat_history = ""
        user_prompt = engine.load_prompt("intent", question=utterance, chat_history=chat_history)
        return await self.llm.chat(self.model, intent_format, user_prompt=user_prompt, return_json=True)
