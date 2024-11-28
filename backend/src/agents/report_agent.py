from src.agents import Agent, agent
from src.prompts import PromptEngine

engine = PromptEngine()


@agent(
    name="ReportAgent",
    description="This agent is responsible for generating an ESG focused report on a narrative document",
    tools=[],
)
class ReportAgent(Agent):
    async def invoke(self, utterance: str) -> str:
        user_prompt = engine.load_prompt(
            "create-report-user-prompt",
            document_text=utterance)

        system_prompt = engine.load_prompt("create-report-system-prompt")

        return await self.llm.chat(self.model, system_prompt=system_prompt, user_prompt=user_prompt)
