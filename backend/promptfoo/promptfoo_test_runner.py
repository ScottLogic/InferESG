import sys
sys.path.append("../")
from src.prompts.prompting import PromptEngine  # noqa: E402

engine = PromptEngine()


def create_prompt(context):
    config = context["vars"]

    system_prompt_args = config["system_prompt_args"] if "system_prompt_args" in config else {}

    system_prompt = engine.load_prompt(template_name=config["system_prompt_template"], **system_prompt_args)

    if "user_prompt" in config:
        user_prompt = config["user_prompt"]
    elif "user_prompt_template" in config:
        user_prompt_args = config["user_prompt_args"] if "user_prompt_args" in config else {}
        user_prompt = engine.load_prompt(template_name=config["user_prompt_template"], **user_prompt_args)
    else:
        raise Exception("Must provide either user_prompt or user_prompt_template")

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
