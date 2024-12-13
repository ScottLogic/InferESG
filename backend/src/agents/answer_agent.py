from datetime import datetime
from src.utils import get_scratchpad
from src.prompts import PromptEngine
from src.agents import ChatAgent, chat_agent
from src.session import get_session_chat

engine = PromptEngine()


@chat_agent(
    name="AnswerAgent",
    description="This agent is responsible for generating an answer for the user, based on results in the scratchpad",
    tools=[],
)
class AnswerAgent(ChatAgent):
    async def invoke(self, utterance: str) -> str:
        final_scratchpad = get_scratchpad()
        create_answer = engine.load_prompt(
            "create-answer",
            chat_history=get_session_chat(),
            final_scratchpad=final_scratchpad,
            datetime=datetime.now()
        )

        return await self.llm.chat(self.model, create_answer, user_prompt=utterance)
