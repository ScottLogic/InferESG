from contextlib import asynccontextmanager
import json
import logging
import logging.config
import os
from typing import NoReturn
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.graph_db_utils import populate_db
from src.utils import Config, test_connection
from src.director import question, dataset_upload
from src.websockets.connection_manager import connection_manager, parse_message
from src.session import RedisSessionMiddleware
from src.suggestions_generator import generate_suggestions

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.ini"))
logging.config.fileConfig(fname=config_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # get file
        # ask LLM to create cypher query
            # create an agent for this
        # promptfoo tests on llm prompt for cypher query
        await dataset_upload()
    except Exception as e:
        logger.exception(f"Failed to populate database with initial data from file: {e}")
    yield


app = FastAPI(lifespan=lifespan)

origins = [config.frontend_url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RedisSessionMiddleware)

health_prefix = "InferESG healthcheck: "
further_guidance = "Please check the README files for further guidance."

healthy_response = health_prefix + "backend is healthy. Neo4J is healthy."
unhealthy_backend_response = health_prefix + "backend is unhealthy. Unable to healthcheck Neo4J. " + further_guidance
unhealthy_neo4j_response = health_prefix + "backend is healthy. Neo4J is unhealthy. " + further_guidance

chat_fail_response = "Unable to generate a response. Check the service by using the keyphrase 'healthcheck'"
suggestions_failed_response = "Unable to generate suggestions. Check the service by using the keyphrase 'healthcheck'"


@app.get("/health")
async def health_check():
    response = JSONResponse(status_code=200, content=healthy_response)
    try:
        if not test_connection():
            response = JSONResponse(status_code=500, content=unhealthy_neo4j_response)
    except Exception as e:
        logger.exception(f"Healthcheck method failed with error: {e}")
        response = JSONResponse(status_code=500, content=unhealthy_neo4j_response)
    finally:
        return response


@app.get("/chat")
async def chat(utterance: str):
    logger.info(f"Chat method called with utterance: {utterance}")
    try:
        final_result = await question(utterance)
        return JSONResponse(status_code=200, content=final_result)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=chat_fail_response)


@app.get("/suggestions")
async def suggestions():
    logger.info("Requesting chat suggestions")
    try:
        final_result = await generate_suggestions()
        return JSONResponse(status_code=200, content=final_result)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=suggestions_failed_response)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    await connection_manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_json()
            parsed_message = parse_message(message)
            await connection_manager.handle_message(websocket, parsed_message)
    except Exception:
        await connection_manager.disconnect(websocket)
