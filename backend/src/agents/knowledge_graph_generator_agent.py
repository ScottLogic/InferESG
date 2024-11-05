import logging

from src.prompts import PromptEngine
from src.agents import Agent, agent

logger = logging.getLogger(__name__)
engine = PromptEngine()


@agent(
    name="KnowledgeGraphAgent",
    description="This agent is responsible for generating knowledge graphs to import csv datasets",
    tools=[],
)
class KnowledgeGraphAgent(Agent):
    async def generate_knowledge_graph(self, file_path: str) -> str:

        # load file
        # extract headers and the first couple of lines
        # pass into llm with prompt
        with open(file_path, 'r') as file:
            csv_lines = []
            for line in file:
                csv_lines.append(line)
                if len(csv_lines) >= 50:
                    break

        create_answer = engine.load_prompt(
            "generate-knowledge-graph",
            csv_input=csv_lines
        )

        return await self.llm.chat(self.model, create_answer, user_prompt="")
