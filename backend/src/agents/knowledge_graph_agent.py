import json
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
    async def generate_knowledge_graph(self, csv_data: list[list[str]]) -> dict[str, str]:

        reduced_data_set = csv_data[slice(50)]

        create_model = engine.load_prompt(
            "generate-knowledge-graph-model",
            csv_input=reduced_data_set
        )

        model_response = await self.llm.chat(self.model, create_model, user_prompt="")

        model = json.loads(model_response)["model"]

        create_query = engine.load_prompt(
            "generate-knowledge-graph-query",
            csv_input=reduced_data_set,
            model_input=model
        )

        query_response = await self.llm.chat(self.model, create_query, user_prompt="")

        query = json.loads(query_response)["cypher_query"]
        return {"cypher_query": query, "model": model}
