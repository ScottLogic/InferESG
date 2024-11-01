import sys
import os
sys.path.append("../")
from dotenv import load_dotenv, find_dotenv  # noqa: E402
from src.prompts.prompting import PromptEngine  # noqa: E402

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
engine = PromptEngine()


def generate_message_suggestions(context):
    chat_history = context["vars"]["chatHistory"]

    system_prompt = engine.load_prompt("generate_message_suggestions", chat_history=chat_history)

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Give me 5 suggestions."}]
