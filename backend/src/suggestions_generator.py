import json
from typing import List
from src.llm.factory import get_llm
from src.prompts.prompting import PromptEngine
from src.utils.config import Config
from src.agents.intent_agent import read_file_core

import logging

config = Config()
engine = PromptEngine()
logger = logging.getLogger(__name__)
suggestions_prompt = engine.load_prompt("generate_message_suggestions")
model = config.suggestions_model


async def generate_suggestions() -> List[str]:
    llm = get_llm(config.suggestions_llm)
    model = get_suggestions_model()
    chat_history = await read_file_core("conversation-history.txt")

    suggestions_prompt = engine.load_prompt("generate_message_suggestions", chat_history=chat_history)
    response = await llm.chat(model, suggestions_prompt, user_prompt="Give me 5 suggestions.", return_json=True)
    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        response_json = {"suggestions": []}
    return response_json["suggestions"]


def get_suggestions_model() -> str:
    model = config.suggestions_model
    if model is None:
        raise ValueError("No model name found for the Suggestions LLM.")

    return model
