# src/llm/openai_llm.py
import logging
from .openai_client import OpenAIClient
from src.utils import Config
from .llm import LLM
from openai import NOT_GIVEN, AsyncOpenAI

logger = logging.getLogger(__name__)
config = Config()


async def generate_report() -> str:
    client = AsyncOpenAI(api_key=config.openai_key)

    assistant = await client.beta.assistants.create(
        name="Financial Analyst Assistant",
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

    # assistant = client.beta.assistants.update(
    #     assistant_id=assistant.id,
    #     tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    # )

# Upload the user provided file to OpenAI
    message_file = await client.files.create(
        file=open("./datasets/mcdonalds_2023_esg_report.pdf", "rb"), purpose="assistants",
    )

    # Create a thread and attach the file to the message
    thread = await client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Can you create an ESG report for this document?",
                # Attach the new file to the message.
                "attachments": [
                    { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
                ],
            }
        ]
    )

    run = await client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    # The thread now has a vector store with that file in its tool resources.
    messages = await client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    logger.info(messages)


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

    # async def upload_file(self) -> str:
    #     client = AsyncOpenAI(api_key=config.openai_key)
    #     try:
    #         # Create a vector store called "Financial Statements"
    #         vector_store = AsyncOpenAI.beta.vector_stores.create(name="Sustainability Report")
    #
    #         # Ready the files for upload to OpenAI
    #         file_paths = ["./datasets/mcdonalds_2023_esg_report.pdf"]
    #         file_streams = [open(path, "rb") for path in file_paths]
    #
    #         # Use the upload and poll SDK helper to upload the files, add them to the vector store,
    #         # and poll the status of the file batch for completion.
    #         file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
    #             vector_store_id=vector_store.id, files=file_streams
    #         )
    #
    #         # You can print the status and the file counts of the batch to see the result of this operation.
    #         print(file_batch.status)
    #         print(file_batch.file_counts)
    #     except Exception as e:
    #         logger.error(f"Error calling OpenAI model: {e}")
    #         return "An error occurred while processing the request."
