from src.agents import Agent, agent
from src.prompts import PromptEngine

engine = PromptEngine()


@agent(
    name="ESGReportAgent",
    description="This agent is responsible for generating an ESG report",
    tools=[],
)
class ESGReportAgent(Agent):
    async def invoke(self, document_text: str) -> str:
        user_prompt = engine.load_prompt(
            "esg-report-user-prompt",
            document_text=document_text)

        system_prompt = engine.load_prompt(
            "create-esg-report",
        )

        return await self.llm.chat(self.model, system_prompt=system_prompt, user_prompt=user_prompt)