from uuid import uuid4
import pytest
from unittest.mock import patch, MagicMock
from src.session import get_session_cypher_query, update_session_cypher_query, clear_session_cypher_query

@pytest.fixture
def mock_request_context():
    with patch('src.session.redis_session_middleware.request_context'):
        mock_instance = MagicMock()
        mock_instance.get.return_value.state.session = {}
        yield mock_instance


def test_session_cypher_query(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    query_id_1 = uuid4()
    cypher_query_1 = "match(n) return n"

    update_session_cypher_query(query_id_1, cypher_query_1)
    query_id_2 = uuid4()
    cypher_query_2 = "match(c:Country) return c"

    update_session_cypher_query(query_id_2, cypher_query_2)
    assert get_session_cypher_query() == [
        {"queryid": str(query_id_1), "cypher_query": cypher_query_1},
        {"queryid": str(query_id_2), "cypher_query": cypher_query_2}
    ]


def test_clear_session_cypher_query(mocker, mock_request_context):
    mocker.patch("src.session.redis_session_middleware.request_context", mock_request_context)

    query_id = uuid4()
    cypher_query = "match(n) return n"

    update_session_cypher_query(query_id, cypher_query)
    assert get_session_cypher_query() == [{"queryid": str(query_id), "cypher_query": cypher_query}]
    clear_session_cypher_query()
    assert get_session_cypher_query() == []
