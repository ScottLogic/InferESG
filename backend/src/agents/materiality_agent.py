import json
from pathlib import Path
import logging

from src.llm import LLMFile
from src.agents import ChatAgent, chat_agent
from src.prompts import PromptEngine

engine = PromptEngine()
logger = logging.getLogger(__name__)


def create_llm_files(filenames: list[str]) -> list[LLMFile]:
    return [
        LLMFile(filename=filename, file=Path(f"./library/{filename}"))
        for filename in filenames
    ]


@chat_agent(
    name="MaterialityAgent",
    description="This agent can help answer questions about ESG Materiality, what topics are relevant to a company"
                "or sector and explain materiality topics in detail. The Materiality Agent can also answer"
                "questions about typical sector activities, value chain and business relationships.",
    tools=[]
)
class MaterialityAgent(ChatAgent):
    async def invoke(self, utterance: str) -> str:
        materiality_files = await self.select_material_files(utterance)
        if materiality_files:
            answer = await self.llm.chat_with_file(
                self.model,
                system_prompt=engine.load_prompt("answer-materiality-question"),
                user_prompt=utterance,
                files=create_llm_files(materiality_files)
            )
        else:
            answer = f"Materiality Agent cannot find suitable reference documents to answer the question: {utterance}"
        return json.dumps({"content": answer, "ignore_validation": False})

    async def list_material_topics_for_company(self, company_name: str) -> dict[str, str]:
        materiality_files = await self.select_material_files(company_name)
        if not materiality_files:
            logger.info(f"No materiality reference documents could be found for {company_name}")
            return {}
        materiality_topics = await self.llm.chat_with_file(
            self.model,
            system_prompt=engine.load_prompt("list-material-topics-system-prompt"),
            user_prompt=f"What topics are material for {company_name}?",
            files=create_llm_files(materiality_files)
        )
        return json.loads(materiality_topics)["material_topics"]

    async def select_material_files(self, utterance) -> list[str]:
        with open('./library/catalogue.json') as file:
            catalogue = json.load(file)
            files_json = await self.llm.chat(
                self.model,
                system_prompt=engine.load_prompt(
                    "select-material-files-system-prompt",
                    catalogue=catalogue
                ),
                user_prompt=utterance,
                return_json=True
            )
            return json.loads(files_json)["files"]
