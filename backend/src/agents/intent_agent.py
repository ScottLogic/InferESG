from src.prompts import PromptEngine
from src.agents import Agent, agent
from src.session import get_session_chat
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
        user_prompt = engine.load_prompt("intent", question=utterance, chat_history=get_session_chat())
        return await self.llm.chat(self.model, intent_format, user_prompt=user_prompt, return_json=True)
