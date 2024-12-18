from src.prompts import PromptEngine
from src.agents import ChatAgent, chat_agent
from src.session import get_session_chat
from src.session.file_uploads import get_uploaded_report_content
import logging
from src.utils.config import Config


config = Config()

engine = PromptEngine()
intent_system = engine.load_prompt("intent-system")
logger = logging.getLogger(__name__)


@chat_agent(
    name="IntentAgent",
    description="This agent is responsible for determining the intent of the user's utterance",
    tools=[],
)
class IntentAgent(ChatAgent):
    async def invoke(self, utterance: str) -> str:
        session_chat = get_session_chat()
        session_report_content = get_uploaded_report_content()
        user_prompt = engine.load_prompt(
            "intent", question=utterance, chat_history=session_chat if session_chat else "There is no chat history",
            report_content=session_report_content if session_report_content else "There is no report content"
        )
        return await self.llm.chat(self.model, intent_system, user_prompt=user_prompt, return_json=True)
