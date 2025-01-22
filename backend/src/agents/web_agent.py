import logging
from src.prompts import PromptEngine
from src.agents.agent import chat_agent
from src.agents.base_chat_agent import BaseChatAgent
from src.agents.tool import tool, Parameter, ToolActionSuccess, ToolActionFailure
from src.utils import Config
from src.utils.web_utils import (
    search_urls,
    scrape_content,
    summarise_content,
    summarise_pdf_content
)
import aiohttp
import io
from pypdf import PdfReader
import json
from typing import Any

logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


async def web_general_search_core(search_query, llm, model) -> ToolActionSuccess | ToolActionFailure:
    search_result_json = await search_urls(search_query, num_results=15)
    search_result = json.loads(search_result_json)

    if search_result.get("status") == "error":
        return ToolActionFailure("No relevant information found on the internet for the given query.")
    urls = search_result.get("urls", [])
    logger.info(f"URLs found: {urls}")

    summaries = []
    for url in urls:
        content = await perform_scrape(url)
        if not content:
            continue  # Skip to the next URL if no content is found
        summary = await summarise_content(search_query, content, llm, model)

        if summary:
            summaries.append({"answer": summary, "citation_url": url})
            if len(summaries) >= 3:
                break
        else:
            logger.info(f"No relevant content found for url: {url}")
    if summaries:
        return ToolActionSuccess(summaries)
    else:
        return ToolActionFailure("No relevant information found on the internet for the given query.")


async def web_pdf_download_core(pdf_url, llm, model) -> ToolActionSuccess | ToolActionFailure:
    try:
        async with aiohttp.request("GET", url=pdf_url) as response:
            content = await response.read()
            on_fly_mem_obj = io.BytesIO(content)
            pdf_file = PdfReader(on_fly_mem_obj)
            all_content = ""
            for page_num in range(len(pdf_file.pages)):
                page_text = pdf_file.pages[page_num].extract_text()
                summary = await perform_pdf_summarization(page_text, llm, model)
                if not summary:
                    continue
                parsed_json = json.loads(summary)
                summary = parsed_json.get("summary", "")
                all_content += summary
                all_content += "\n"
            logger.info("PDF content extracted successfully")
            response = {"content": all_content, "ignore_validation": "true"}
        return ToolActionSuccess(response)
    except Exception as e:
        logger.error(f"Error in web_pdf_download_core: {e}")
        return ToolActionFailure("An error occurred while processing the search query.")


@tool(
    name="web_general_search",
    description=(
        "Search the internet based on the query provided and then get the meaningful answer from the content found"
    ),
    parameters={
        "search_query": Parameter(
            type="string",
            description="The search query to find information on the internet",
        ),
    },
)
async def web_general_search(search_query, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return await web_general_search_core(search_query, llm, model)


@tool(
    name="web_pdf_download",
    description=("Download the data from the provided pdf url"),
    parameters={
        "pdf_url": Parameter(
            type="string",
            description="The pdf url to find information on the internet",
        ),
    },
)
async def web_pdf_download(pdf_url, llm, model) -> ToolActionSuccess | ToolActionFailure:
    return await web_pdf_download_core(pdf_url, llm, model)


async def web_scrape_core(url: str) -> ToolActionSuccess | ToolActionFailure:
    try:
        # Scrape the content from the provided URL
        content = await perform_scrape(url)
        if not content:
            return ToolActionFailure("No content found at the provided URL.")
        logger.info(f"Content scraped successfully: {content}")
        content = content.replace("\n", " ").replace("\r", " ")
        response = {"content": {"content": content, "url": url}, "ignore_validation": "true"}
        return ToolActionSuccess(response)
    except Exception as e:
        return ToolActionFailure(str(e))


@tool(
    name="web_scrape",
    description="Scrapes the content from the given URL.",
    parameters={
        "url": Parameter(
            type="string",
            description="The URL of the page to scrape the content from.",
        ),
    },
)
async def web_scrape(url: str, llm, model) -> ToolActionSuccess | ToolActionFailure:
    logger.info(f"Scraping the content from URL: {url}")
    return await web_scrape_core(url)


async def perform_scrape(url: str) -> str:
    try:
        if not str(url).startswith("https"):
            return ""
        scrape_result_json = await scrape_content(url, )
        scrape_result = json.loads(scrape_result_json)
        if scrape_result["status"] == "error":
            return ""
        return scrape_result["content"]
    except Exception as e:
        logger.error(f"Error scraping content from {url}: {e}")
        return ""


async def perform_pdf_summarization(content: str, llm: Any, model: str) -> str:
    try:
        summarise_result_json = await summarise_pdf_content(content, llm, model)
        summarise_result = json.loads(summarise_result_json)
        if summarise_result["status"] == "error":
            return ""
        return summarise_result["response"]
    except Exception as e:
        logger.error(f"Error summarizing content: {e}")
        return ""


@chat_agent(
    name="WebAgent",
    description="This agent can search the internet to answer questions which require current information or general "
                "ESG or company related questions.",
    tools=[web_general_search],
)
class WebAgent(BaseChatAgent):
    pass
