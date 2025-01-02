import pytest
from unittest.mock import MagicMock
from neo4j import Driver, Record, Session
from src.utils.graph_db_utils import is_db_populated, populate_db
from src.utils import test_connection as verify_connection


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    session.run = MagicMock()
    session.close = MagicMock()
    return session


@pytest.fixture
def mock_driver(mock_session):
    driver = MagicMock(spec=Driver)
    driver.session.return_value.__enter__.return_value = mock_session
    driver.session.return_value.__exit__.return_value = None
    driver.close = MagicMock()
    return driver


def remove_whitespace_and_newlines(original):
    return " ".join(original.replace(r"\n", " ").replace(r"\r", "").split())


def test_database_connectivity_is_healthy(mocker, mock_driver):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)
    mock_driver.verify_connectivity.return_value = None

    connected = verify_connection()

    assert connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_database_connectivity_is_unhealthy(mocker, mock_driver):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)
    mock_driver.verify_connectivity.side_effect = Exception

    connected = verify_connection()

    assert not connected
    mock_driver.verify_connectivity.assert_called_once()
    mock_driver.close.assert_called_once()


def test_populate_db_populates_db(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    query = "CREATE (n:Test {data: $all_data})"
    data = {"key": "value"}

    populate_db(query, data)

    mock_session.run.assert_any_call("MATCH (n) DETACH DELETE n")
    mock_session.run.assert_any_call(query, data={"all_data": data})

    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()


def test_populate_db_throws_exception(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    query = "CREATE (n:Test {data: $all_data})"
    data = {"key": "value"}

    mock_session.run.side_effect = Exception("Test exception")

    with pytest.raises(Exception, match="Test exception"):
        populate_db(query, data)

    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()

def test_is_db_populated_returns_true(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    class RecordEntryMock:
        def data(self):
            return {"key": "value"}

    record = Record([("a", RecordEntryMock())])

    mock_session.run.return_value = record

    assert is_db_populated()
    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()

def test_is_db_populated_returns_false(mocker, mock_driver, mock_session):
    mocker.patch("src.utils.graph_db_utils.driver", mock_driver)

    mock_session.run.return_value = Record([])

    assert not is_db_populated()
    mock_driver.session.return_value.__exit__.assert_called_once()
    mock_driver.close.assert_called_once()
