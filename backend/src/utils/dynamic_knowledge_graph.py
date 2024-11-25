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

    model_system_prompt = engine.load_prompt("generate-knowledge-graph-model")

    model_response = await llm.chat(
        llm_model,  # type: ignore[reportArgumentType]
        model_system_prompt,
        user_prompt=str(reduced_data_set)
    )

    data_model = json.loads(model_response)["model"]

    system_prompt = engine.load_prompt("generate-knowledge-graph-cypher-system-prompt")
    user_prompt = engine.load_prompt(
        "generate-knowledge-graph-cypher-user-prompt",
        input_data=reduced_data_set,
        data_model=data_model
    )

    query_response = await llm.chat(
        llm_model,  # type: ignore[reportArgumentType]
        system_prompt,
        user_prompt=user_prompt
    )

    query = json.loads(query_response)["cypher_query"]
    return {"cypher_query": query, "model": data_model}
