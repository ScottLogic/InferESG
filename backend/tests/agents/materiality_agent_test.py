from unittest.mock import patch, mock_open

import pytest
import json

from src.agents.materiality_agent import MaterialityAgent
from src.llm.factory import get_llm

mock_model = "mockmodel"
mock_llm = get_llm("mockllm")
mock_selected_files = {"files": ["file1.pdf", "file2.pdf"]}

mock_materiality_topics = {"material_topics": {"topic1": "topic1 description", "topic2": "topic2 description"}}

mock_catalogue = {
    "library": {
        "Standard1": [{"name": "name"}],
        "Standard2": [{"name2": "name2"}],
    }
}


@pytest.mark.asyncio
async def test_invoke_calls_llm(mocker):
    agent = MaterialityAgent(llm_name="mockllm", model=mock_model)

    with patch("builtins.open", mock_open(read_data=json.dumps(mock_catalogue))):
        mock_llm.chat = mocker.AsyncMock(return_value=json.dumps(mock_selected_files))
        mock_llm.chat_with_file = mocker.AsyncMock(return_value=json.dumps(mock_materiality_topics))

        response = await agent.list_material_topics("AstraZeneca")

        assert response == mock_materiality_topics["material_topics"]
