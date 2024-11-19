import sys
sys.path.append("../")
from src.prompts.prompting import PromptEngine  # noqa: E402

engine = PromptEngine()


def create_prompt(context):
    system_prompt_args = context["vars"]["system_prompt_args"]
    system_prompt_template = context["vars"]["system_prompt_template"]
    user_prompt = context["vars"]["user_prompt"]

    system_prompt = engine.load_prompt(template_name=system_prompt_template, **system_prompt_args)

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
