from src.api import app
from src.utils import Config
from fastapi.testclient import TestClient
from langchain.evaluation import EvaluatorType, StringEvaluator, load_evaluator
from langchain_openai.chat_models import ChatOpenAI

START_ENDPOINT_URL = "/chat?utterance={utterance}"
CONVERSATION_ENDPOINT_URL = "/chat?utterance={utterance}"
HEALTHCHECK_ENDPOINT_URL = "/health"
health_prefix = "InferESG healthcheck: "
healthy_response = health_prefix + "backend is healthy. Neo4J is healthy."

client = TestClient(app)
config = Config()


def app_healthcheck():
    healthcheck_response = client.get(HEALTHCHECK_ENDPOINT_URL)
    return healthcheck_response


async def send_prompt(prompt: str):
    start_response = client.get(START_ENDPOINT_URL.format(utterance=prompt))
    return start_response

# Evaluators
# Evaluation LLM
llm = ChatOpenAI(api_key=config.openai_key, model="gpt-4o-mini", temperature=0, max_retries=2) # type: ignore

correctness_evaluator: StringEvaluator = load_evaluator(  # type: ignore
    EvaluatorType.LABELED_CRITERIA, criteria="correctness", llm=llm
)

confidence_criterion = {
    "confidence": "Does the bot seem confident that it replied to the question and gave the correct answer?"
}

confidence_evaluator: StringEvaluator = load_evaluator(  # type: ignore
    EvaluatorType.CRITERIA, criteria=confidence_criterion, llm=llm
)


def check_response_confidence(prompt: str, bot_response: str) -> dict[str, str]:
    """
    Uses an LLM to check the confidence of the bot's response.\n
    Returns a dictionary with the binary score (pass = 1, fail = 0) and reasoning (text format)."""
    return confidence_evaluator.evaluate_strings(
        input=prompt,
        prediction=bot_response,
    )
