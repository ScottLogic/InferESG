from prompting import PromptEngine

engine = PromptEngine()


def get_prompt(context):
    chat_history = context["vars"]["chatHistory"]

    system_prompt = engine.load_prompt("generate_message_suggestions", chat_history=chat_history)

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Give me 5 suggestions."}]
