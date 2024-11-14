import json
import logging

from src.llm.factory import get_llm
from src.prompts import PromptEngine
from src.utils import Config

logger = logging.getLogger(__name__)
engine = PromptEngine()
config = Config()

llm_model = config.dynamic_knowledge_graph_model


async def generate_dynamic_knowledge_graph(csv_data: list[list[str]]) -> dict[str, str]:
    llm = get_llm(config.dynamic_knowledge_graph_llm)

    reduced_data_set = csv_data[slice(50)]

    create_model = engine.load_prompt(
        "generate-knowledge-graph-model",
        csv_input=reduced_data_set
    )

    model_response = await llm.chat(llm_model, create_model, user_prompt="")

    kg_model = json.loads(model_response)["model"]

    create_query = engine.load_prompt(
        "generate-knowledge-graph-query",
        csv_input=reduced_data_set,
        model_input=kg_model
    )

    query_response = await llm.chat(llm_model, create_query, user_prompt="")

    query = json.loads(query_response)["cypher_query"]
    return {"cypher_query": query, "model": kg_model}
