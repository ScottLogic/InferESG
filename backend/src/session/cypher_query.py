from typing import TypedDict
import uuid
import logging

from .redis_session_middleware import get_session, set_session

logger = logging.getLogger(__name__)

CYPHER_QUERY_SESSION_KEY = "cypher_query"

class CypherQuery(TypedDict):
    queryId: uuid.UUID
    cypher_query: str


def get_session_cypher_query() -> list[CypherQuery] | None:
    return get_session(CYPHER_QUERY_SESSION_KEY, [])


def update_session_cypher_query(queryid=None, cypher_query=None):
    cypher_query_session = get_session(CYPHER_QUERY_SESSION_KEY, [])
    if not cypher_query_session:
        # initialise the session object
        set_session(CYPHER_QUERY_SESSION_KEY, cypher_query_session)

    cypher_query_session.append({"queryid": str(queryid), "cypher_query": cypher_query})


def clear_session_cypher_query():
    logger.info("Cypher query session cleared")
    set_session(CYPHER_QUERY_SESSION_KEY, [])
