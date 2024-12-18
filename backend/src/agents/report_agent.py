import json
import logging

from src.llm.llm import LLMFile
from src.agents import Agent
from src.prompts import PromptEngine

logger = logging.getLogger(__name__)
engine = PromptEngine()


class ReportAgent(Agent):
    async def create_report(self, file: LLMFile, materiality_topics: dict[str, str]) -> str:
        return await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("create-report-system-prompt"),
            user_prompt=engine.load_prompt("create-report-user-prompt", materiality_topics=materiality_topics),
            files=[file],
        )

    async def get_company_name(self, file: LLMFile) -> str:
        response = await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("find-company-name-from-file-system-prompt"),
            user_prompt=engine.load_prompt("find-company-name-from-file-user-prompt"),
            files=[file],
        )
        return json.loads(response)["company_name"]
