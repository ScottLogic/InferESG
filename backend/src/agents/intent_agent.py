from src.prompts import PromptEngine
from src.agents import Agent
from src.session import get_session_chat
import logging
from src.utils.config import Config


config = Config()

engine = PromptEngine()
intent_system = engine.load_prompt("intent-system")
logger = logging.getLogger(__name__)


class IntentAgent(Agent):
    async def determine_intent(self, utterance: str) -> str:
        session_chat = get_session_chat()
        user_prompt = engine.load_prompt(
            "intent", question=utterance, chat_history=session_chat if session_chat else "There is no chat history"
        )
        return await self.llm.chat(self.model, intent_system, user_prompt=user_prompt, return_json=True)
