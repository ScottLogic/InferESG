import logging
from neo4j import GraphDatabase
from src.utils import Config

logger = logging.getLogger(__name__)

config = Config()

URI = config.neo4j_uri
AUTH = (config.neo4j_user, config.neo4j_password)

driver = GraphDatabase.driver(URI, auth=AUTH)


def test_connection():
    connection_healthy = False
    try:
        driver.verify_connectivity()
        connection_healthy = True

    except Exception as e:
        logger.exception(f"Database connection failed: {e}")

    finally:
        driver.close()
        return connection_healthy


def execute_query(llm_query):
    try:
        with driver.session() as session:
            query = llm_query
            records = session.run(query)
            record_dict = [record.data() for record in records]
            return record_dict

    except Exception as e:
        logger.exception(f"Error: {e}")
        raise

    finally:
        driver.close()


def populate_db(query, data) -> None:
    data = {"all_data": data}
    try:
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.debug("Cleared database")

            session.run(query, data=data)
            logger.debug("Database populated")
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise
    finally:
        driver.close()
