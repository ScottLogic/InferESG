import logging
from src.prompts import PromptEngine
from src.agents.agent import chat_agent
from src.agents.base_chat_agent import BaseChatAgent
from src.agents.tool import Parameter, parameterised_tool, ToolActionSuccess, ToolActionFailure, ToolAnswerType
from src.llm.llm import LLM
from io import BytesIO
import base64
from src.utils import scratchpad
from PIL import Image
# from src.websockets.user_confirmer import UserConfirmer
# from src.websockets.confirmations_manager import confirmations_manager

logger = logging.getLogger(__name__)

engine = PromptEngine()


async def generate_chart(
    question_intent,
    data_provided,
    question_params,
    llm: LLM, model
) -> ToolActionSuccess | ToolActionFailure:
    details_to_generate_chart_code = engine.load_prompt(
        "details-to-generate-chart-code",
        question_intent=question_intent,
        data_provided=data_provided,
        question_params=question_params,
        scratchpad=scratchpad,
    )

    generate_chart_code_prompt = engine.load_prompt("generate-chart-code")
    generated_code = await llm.chat(model, generate_chart_code_prompt, details_to_generate_chart_code)
    sanitised_script = sanitise_script(generated_code)

    try:
        # confirmer = UserConfirmer(confirmations_manager)
        is_confirmed = True
        # await confirmer.confirm("Would you like to generate a graph?")
        if not is_confirmed:
            raise Exception("The user did not confirm to creating a graph.")
        local_vars = {}
        exec(sanitised_script, {}, local_vars)
        fig = local_vars.get("fig")
        buf = BytesIO()
        if fig is None:
            raise ValueError("The generated code did not produce a figure named 'fig'.")
        fig.savefig(buf, format="png")
        buf.seek(0)
        with Image.open(buf):
            image_data = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
    except Exception as e:
        logger.error(f"Error during chart generation or saving: {e}")
        raise
    return ToolActionSuccess(image_data)


def sanitise_script(script: str) -> str:
    script = script.strip()
    if script.startswith("```python"):
        script = script[9:]
    if script.endswith("```"):
        script = script[:-3]
    return script.strip()


@parameterised_tool(
    name="generate_code_chart",
    description="Generate Matplotlib bar chart code if the user's query involves creating a chart",
    parameters={
        "question_intent": Parameter(
            type="string",
            description="This represents the overall intent the question is attempting to answer",
        ),
        "data_provided": Parameter(
            type="string",
            description="This is the data collected to answer the user_intent. The data is stored in the scratchpad",
        ),
        "question_params": Parameter(
            type="string",
            description="""
                The specific parameters required for the question to be answered with the question_intent,
                extracted from data_provided
            """,
        ),
    },
)
async def generate_code_chart(
    question_intent,
    data_provided,
    question_params,
    llm: LLM,
    model
) -> ToolActionSuccess | ToolActionFailure:
    return await generate_chart(question_intent, data_provided, question_params, llm, model)


@chat_agent(
    name="ChartGeneratorAgent",
    description="This agent is responsible for creating charts",
    tools=[generate_code_chart],
)
class ChartGeneratorAgent(BaseChatAgent):
    async def validate(self, utterance: str, answer: ToolAnswerType):
        return True
