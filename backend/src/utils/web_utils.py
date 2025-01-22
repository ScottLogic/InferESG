import logging
import random

from googlesearch import search
import aiohttp
from bs4 import BeautifulSoup
from src.prompts import PromptEngine
from src.utils import Config
import json


logger = logging.getLogger(__name__)
config = Config()

engine = PromptEngine()


def create_fake_headers() -> dict[str, str]:
    user_agents = ["Macintosh; Intel Mac OS X 10_15_7", "Windows NT 10.0; Win64; x64"]
    return {
        "User-Agent": f"Mozilla/5.0 ({random.choice(user_agents)}) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }


async def search_urls(search_query, num_results=10) -> str:
    logger.info(f"Searching the web for: {search_query}")
    try:
        urls = search(search_query, num_results=99)
        https_urls = [str(url) for url in urls if str(url).startswith("https")]
        return json.dumps(
            {
                "status": "success",
                "urls": https_urls[:num_results],
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during web search: {e}")
        return json.dumps(
            {
                "status": "error",
                "urls": [],
                "error": str(e),
            }
        )


async def scrape_content(url, limit=100000) -> str:
    try:
        logger.info(f"Scraping content from URL: {url}")
        async with aiohttp.request("GET", url, headers=create_fake_headers()) as response:
            response.raise_for_status()
            soup = BeautifulSoup(await response.text(), "html.parser")
            paragraphs_and_tables = soup.find_all(["p", "table", "h1", "h2", "h3", "h4", "h5", "h6"])
            content = "\n".join([tag.get_text() for tag in paragraphs_and_tables])
            return json.dumps(
                {
                    "status": "success",
                    "content": content[:limit],
                    "error": None,
                }
            )
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return json.dumps(
            {
                "status": "error",
                "content": "",
                "error": str(e),
            }
        )


async def summarise_content(search_query, contents, llm, model) -> str | None:
    response = json.loads(await llm.chat(
        model,
        engine.load_prompt("web_page_scrape_summary_system_prompt", question=search_query, content=contents),
        "",
        return_json=True
    ))
    if "relevant" in response and response["relevant"].lower() == "true" and "summary" in response:
        return response["summary"]
    return None


async def summarise_pdf_content(contents, llm, model) -> str:
    try:
        summariser_prompt = engine.load_prompt("pdf-summariser", content=contents)
        response = await llm.chat(model, summariser_prompt, "", return_json=True)
        return json.dumps(
            {
                "status": "success",
                "response": response,
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during summarisation of PDF: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )


async def perform_math_operation_util(math_query, llm, model) -> str:
    try:
        math_prompt = engine.load_prompt("math-solver", query=math_query)
        response = await llm.chat(model, math_prompt, "", return_json=True)
        logger.info(f"Math operation response: {response}")
        return json.dumps(
            {
                "status": "success",
                "response": response,  # math result
                "error": None,
            }
        )
    except Exception as e:
        logger.error(f"Error during math operation: {e}")
        return json.dumps(
            {
                "status": "error",
                "response": None,
                "error": str(e),
            }
        )
