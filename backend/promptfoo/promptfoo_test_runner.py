import sys
from pypdf import PdfReader

sys.path.append("../")
from src.prompts.prompting import PromptEngine  # noqa: E402

engine = PromptEngine()


def read_pdf_file_for_promptfoo(file_path: str) -> str:
    pdf_file = PdfReader(file_path)
    content = "\n".join([page.extract_text() for page in pdf_file.pages])
    return content


def create_prompt(context):
    config = context["vars"]

    if "system_prompt" in config:
        system_prompt = config["system_prompt"]
    else:
        system_prompt_args = config["system_prompt_args"] if "system_prompt_args" in config else {}

        system_prompt = engine.load_prompt(template_name=config["system_prompt_template"], **system_prompt_args)

    if "user_prompt" in config:
        user_prompt = config["user_prompt"]
    elif "user_prompt_template" in config:
        user_prompt_args = config["user_prompt_args"] if "user_prompt_args" in config else {}
        user_prompt = engine.load_prompt(template_name=config["user_prompt_template"], **user_prompt_args)
    else:
        raise Exception("Must provide either user_prompt or user_prompt_template")

    if "file_attachment" in config:
        user_prompt = f"{user_prompt}\n\nAttached file: {read_pdf_file_for_promptfoo(config["file_attachment"])}"

    return [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
