import json
from typing import List
from src.llm.factory import get_llm
from src.prompts.prompting import PromptEngine
from src.session import Message, get_session_chat
from src.session.file_uploads import get_uploaded_report
from src.utils.config import Config
import logging

config = Config()
engine = PromptEngine()
suggestions_prompt = engine.load_prompt("generate-message-suggestions")
model = config.suggestions_model
logger = logging.getLogger(__name__)


async def generate_suggestions() -> List[str]:
    llm = get_llm(config.suggestions_llm)
    model = get_suggestions_model()
    chat_history = get_chat_history()
    uploaded_report = get_uploaded_report()
    report_content = uploaded_report["report"] if uploaded_report else "There is no report content"

    response = await llm.chat(
        model,
        engine.load_prompt(
            "generate-message-suggestions", chat_history=chat_history, report_content=report_content
        ),
        user_prompt="Give me 5 suggestions.",
        return_json=True
    )
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


def get_chat_history() -> List[str] | str:
    max_history_length = 4
    raw_history = get_session_chat()

    if raw_history is None:
        return "No chat history available."

    if len(raw_history) > max_history_length:
        raw_history = raw_history[-max_history_length:]

    natural_language_history = remove_datasets_from_history(raw_history)
    return natural_language_history


def remove_datasets_from_history(history: list[Message]) -> List[str]:
    filtered = []
    for message in history:
        if message["role"] == "user":
            filtered.append(f"User: {message['content']}")
        else:
            if message["content"] is not None:
                try:
                    natural_language_answer = json.loads(message["content"])
                    filtered.append(
                        f"System: {natural_language_answer['final_answer']}")
                except json.JSONDecodeError:
                    filtered.append(f"System: {message['content']}")

    return filtered
