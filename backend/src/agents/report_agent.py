from src.llm.llm import LLMFileFromBytes
from src.agents import Agent
from src.prompts import PromptEngine

engine = PromptEngine()


class ReportAgent(Agent):
    async def create_report(self, file: LLMFileFromBytes) -> str:
        user_prompt = engine.load_prompt("create-report-user-prompt")
        system_prompt = engine.load_prompt("create-report-system-prompt")

        return await self.llm.chat_with_file(
            self.model, system_prompt=system_prompt, user_prompt=user_prompt, files_by_path=[], files_by_stream=[file]
        )
