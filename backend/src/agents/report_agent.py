import json
import logging

from src.agents import Agent
from src.prompts import PromptEngine

logger = logging.getLogger(__name__)
engine = PromptEngine()


class ReportAgent(Agent):
    async def create_report(self, file_content: str, materiality_topics: dict[str, str]) -> str:
        user_prompt = engine.load_prompt(
            "create-report-user-prompt",
            document_text=file_content,
            materiality_topics=materiality_topics
        )

        system_prompt = engine.load_prompt("create-report-system-prompt")

        return await self.llm.chat(self.model, system_prompt=system_prompt, user_prompt=user_prompt)

    async def get_company_name(self, file_content: str) -> str:
        response = await self.llm.chat(
            self.model,
            system_prompt=engine.load_prompt("find-company-name-from-file-system-prompt"),
            user_prompt=engine.load_prompt(
                "find-company-name-from-file-user-prompt",
                file_content=file_content
            ),
            return_json=True
        )
        return json.loads(response)["company_name"]
