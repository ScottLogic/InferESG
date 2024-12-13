import json
from pathlib import Path
import logging

from src.llm import LLMFile
from src.agents import Agent
from src.prompts import PromptEngine

engine = PromptEngine()
logger = logging.getLogger(__name__)


class MaterialityAgent(Agent):
    async def list_material_topics(self, company_name: str) -> dict[str, str]:
        with open('./library/catalogue.json') as file:
            catalogue = json.load(file)
            files_json = await self.llm.chat(
                self.model,
                system_prompt=engine.load_prompt(
                    "select-material-files-system-prompt",
                    catalogue=catalogue
                ),
                user_prompt=company_name,
                return_json=True
            )

            materiality_topics = await self.llm.chat_with_file(
                self.model,
                system_prompt=engine.load_prompt("list-material-topics-system-prompt"),
                user_prompt=f"What topics are material for {company_name}?",
                files=[
                    LLMFile(file_name=file_name, file=Path(f"./library/{file_name}"))
                    for file_name in json.loads(files_json)["files"]
                ]
            )
            return json.loads(materiality_topics)["material_topics"]
