# src/llm/openai_llm.py
import logging

from openai.types import FileObject
from openai.types.beta.threads.runs import FileSearchToolCall, ToolCallsStepDetails

from .openai_client import OpenAIClient
from src.utils import Config
from .llm import LLM
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()


async def generate_report():
    client = AsyncOpenAI(api_key=config.openai_key)

    citation_assistant = await client.beta.assistants.create(
        name="Report Citation Analyst",
        instructions="""You are a expert at cross-referencing reports against source material and validating citations.
        
Your task is to review an ESG report and match citations to quotes in the source file.
Citations will be in the format: 【1:23†file_name】 where "1:23" is an example citation number.

You will output the quote that you find verbatim (copied exactly, without any additional commentary) for each citation.

If you believe that a report statement being cited is innaccurate after searching the file, you will output "False statement".

Output your results as a json object:
{ "citations": { "CITATION_NUMBER": "QUOTE_FROM_FILE" or "No evidence to support this claim" } }

Do not include any markdown in your output.

Important Notes:
* Some citation numbers might appear multiple times, you must treat duplicate citation numbers as unique instances.
         """,
        model="gpt-4o-mini",
        tools=[{"type": "file_search"}],
    )
    file_assistant = await client.beta.assistants.create(
        name="ESG Analyst",
        instructions="""The user will provide a report from a company. Your goal is to analyse the document and respond answering the following questions in the format described below:

Basic:

1. What is the name of the company that this document refers to?
2. What year or years does the information refer too?
3. Summarise in one sentence what the document is about?

ESG (Environment, Social, Governance:
1. Which aspects of ESG does this document primarily discuss, respond with a percentage of each topic covered by the document.
2. What aspects of ESG are not discussed in the document?

Environmental:

1. What environmental goals does this document describe?
2. What beneficial environmental claims does the company make?
3. What potential environment greenwashing can you identify that should be fact checked?
4. What environmental regulations, standards or certifications can you identify in the document?

Social:

1. What social goals does this document describe?
2. What beneficial societal claims does the company make?
3. What potential societal greenwashing can you identify that should be fact checked?
4. What societal regulations, standards or certifications can you identify in the document?

Governance:

1. What governance goals does this document describe?
2. What beneficial governance claims does the company make?
3. What potential governance greenwashing can you identify that should be fact checked?
4. What governance regulations, standards or certifications can you identify in the document?

Conclusion:

1. What is your conclusion about the claims and potential greenwashing in this document?
2. What are your recommended next steps to verify any of the claims in this document?

The report should be formatted as markdown.""",
        model="gpt-4o",
        tools=[{"type": "file_search"}],
    )

    # sr_file = await client.files.create(
    #     file=open("./datasets/Astra-Zeneca-Sustainability-Report-2023.pdf", "rb"), purpose="assistants",
    # )
    # mm_file = await client.files.create(
    #     file=open("./datasets/Additional-Sector-Guidance-Biotech-and-Pharma.pdf", "rb"), purpose="assistants",
    # )

    thread = await client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Can you create an ESG report for Astra Zeneca's sustainability report that I have attached?",
                "attachments": [
                    {"file_id": "file-BsMEznvJmaRTo2jZnZvf34", "tools": [{"type": "file_search"}]}
                    # {"file_id": sr_file.id, "tools": [{"type": "file_search"}]}
                    # {"file_id": mm_file.id, "tools": [{"type": "file_search"}]}
                ],
            }
        ]
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=file_assistant.id
    )

    logger.info(run)

    # step_list = await client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
    # logger.info(f"step_list {step_list}")
    # step = None
    # for run_step in step_list.data:
    #     if isinstance(run_step.step_details, ToolCallsStepDetails):
    #         for tool in run_step.step_details.tool_calls:
    #             if isinstance(tool, FileSearchToolCall):
    #                 step = await client.beta.threads.runs.steps.retrieve(
    #                     step_id=run_step.id,
    #                     run_id=run.id,
    #                     thread_id=thread.id,
    #                     include=["step_details.tool_calls[*].file_search.results[*].content"]
    #                 )
    #                 logger.info(f"STEP: {step}")
    #
    # if step:
    #     logger.info(step.step_details.tool_calls[0].file_search.results[0].content)

    messages = await client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)

    logger.info(messages)
    report = messages.data[0].content[0].text.value

    thread_2 = await client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"Can you verify the citations in the following report: \n{report}",
                "attachments": [
                    {"file_id": "file-BsMEznvJmaRTo2jZnZvf34", "tools": [{"type": "file_search"}]}
                ]
            }
        ]
    )
    run_2 = await client.beta.threads.runs.create_and_poll(
        thread_id=thread_2.id, assistant_id=citation_assistant.id
    )

    messages_2 = await client.beta.threads.messages.list(thread_id=thread_2.id, run_id=run_2.id)
    logger.info(messages_2)

    # message = await client.beta.threads.messages.retrieve(
    #     thread_id=thread.id,
    #     message_id=messages.data[0].id
    # )
    # logger.info(message)


async def upload_files(file_paths: list[str]) -> list[FileObject]:
    client = AsyncOpenAI(api_key=config.openai_key)

    files = [await client.files.create(file=open(path, "rb"), purpose="assistants") for path in file_paths]

    logger.info(files)
    return files


# async def upload_file_as_vector_store(file_paths: list[str]) -> list[FileObject]:
#     client = AsyncOpenAI(api_key=config.openai_key)
#
#     files = [await client.files.create(file=open(path, "rb"), purpose="assistants") for path in file_paths]
#
#     logger.info(files)
#     return files


class OpenAI(LLM):
    def __init__(self):
        self.client = OpenAIClient()

    async def chat(self, model, system_prompt: str, user_prompt: str, return_json=False) -> str:
        logger.debug(
            "##### Called open ai chat ... llm. Waiting on response model with prompt {0}.".format(
                str([system_prompt, user_prompt])
            )
        )
        client = AsyncOpenAI(api_key=config.openai_key)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0,
                response_format={
                    "type": "json_object"} if return_json else NOT_GIVEN,
            )
            content = response.choices[0].message.content
            logger.info(f"OpenAI response: Finish reason: {response.choices[0].finish_reason}, Content: {content}")
            logger.debug(f"Token data: {response.usage}")

            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(content)
            else:
                return "Unexpected content format"
        except Exception as e:
            logger.error(f"Error calling OpenAI model: {e}")
            return "An error occurred while processing the request."
