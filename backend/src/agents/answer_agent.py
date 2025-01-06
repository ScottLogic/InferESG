from src.utils import get_scratchpad
from src.prompts import PromptEngine

from src.agents import Agent

engine = PromptEngine()


class AnswerAgent(Agent):
    async def create_answer(self, utterance: str) -> str:
        final_scratchpad = get_scratchpad()

        return await self.llm.chat(
            self.model,
            engine.load_prompt("create-answer-system-prompt"),
            engine.load_prompt("create-answer-user-prompt", question=utterance, final_scratchpad=final_scratchpad),
        )
