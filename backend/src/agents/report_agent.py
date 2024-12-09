from src.agents import Agent, agent
from src.prompts import PromptEngine

engine = PromptEngine()


@agent(
    name="ReportAgent",
    description="This agent is responsible for generating an ESG focused report on a narrative document",
    tools=[],
)
class ReportAgent(Agent):
    async def create_report(self, file_content: str, materiality_topics: list[str]) -> str:
        user_prompt = engine.load_prompt(
            "create-report-user-prompt",
            document_text=file_content,
            materiality_topics=materiality_topics
        )

        system_prompt = engine.load_prompt("create-report-system-prompt")

        return await self.llm.chat(self.model, system_prompt=system_prompt, user_prompt=user_prompt)
