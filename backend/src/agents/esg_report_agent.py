from src.agents import Agent, agent
from src.prompts import PromptEngine

engine = PromptEngine()


@agent(
    name="ESGReportAgent",
    description="This agent is responsible for generating an ESG report",
    tools=[],
)
class ESGReportAgent(Agent):
    async def invoke(self, utterance: str) -> str:
        user_prompt = engine.load_prompt(
            "create-esg-report-user-prompt",
            document_text=utterance)

        system_prompt = engine.load_prompt(
            "create-esg-report-system-prompt",
        )

        return await self.llm.chat(self.model, system_prompt=system_prompt, user_prompt=user_prompt)
