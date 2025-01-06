from src.utils import get_scratchpad
from src.prompts import PromptEngine
from src.agents import ChatAgent, chat_agent

engine = PromptEngine()


@chat_agent(
    name="AnswerAgent",
    description="This agent is responsible for generating an answer for the user, based on results in the scratchpad",
    tools=[],
)
class AnswerAgent(ChatAgent):
    async def invoke(self, utterance: str) -> str:
        final_scratchpad = get_scratchpad()

        return await self.llm.chat(
            self.model,
            engine.load_prompt("create-answer-system-prompt"),
            engine.load_prompt("create-answer-user-prompt", question=utterance, final_scratchpad=final_scratchpad),
        )
