import pytest
from unittest.mock import patch, AsyncMock
import json
from src.agents.web_agent import perform_scrape
from src.utils.web_utils import search_urls


@pytest.mark.asyncio
@patch("src.utils.web_utils.search")
async def test_https_urls(mock_search):
    mock_search.return_value = ["https://example.com", "http://nonsecure.com", "https://another-secure-site.com"]

    result = await search_urls("query", num_results=5)
    expected_result = {
        "status": "success",
        "urls": ["https://example.com", "https://another-secure-site.com"],
        "error": None,
    }
    assert json.loads(result) == expected_result


@pytest.mark.asyncio
@patch("src.agents.web_agent.scrape_content", new_callable=AsyncMock)
async def test_perform_scrape_http_url(mock_scrape_content):
    mock_scrape_content.return_value = json.dumps({"status": "success", "content": "Scraped content."})

    result = await perform_scrape("http://nonsecure.com")
    assert result == ""


@pytest.mark.asyncio
@patch("src.agents.web_agent.scrape_content", new_callable=AsyncMock)
async def test_perform_scrape_https_url(mock_scrape_content):
    mock_scrape_content.return_value = json.dumps({"status": "success", "content": "Scraped content."})

    result = await perform_scrape("https://secure.com")
    assert result == "Scraped content."
