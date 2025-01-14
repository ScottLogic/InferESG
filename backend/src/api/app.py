from contextlib import asynccontextmanager
import json
import logging.config
import os
from typing import NoReturn
import uuid
from fastapi import BackgroundTasks, FastAPI, HTTPException, Response, WebSocket, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.session.llm_file_upload import get_llm_file_upload_id
from src.utils.scratchpad import ScratchPadMiddleware
from src.session.chat_response import get_session_chat_response_ids
from src.chat_storage_service import clear_chat_messages, get_chat_message
from src.directors.report_director import create_report_from_file
from src.session.file_uploads import clear_session_file_uploads, get_report
from src.session.redis_session_middleware import reset_session
from src.utils import Config, test_connection
from src.directors.chat_director import question, dataset_upload
from src.websockets.connection_manager import connection_manager, parse_message
from src.session import RedisSessionMiddleware
from src.suggestions_generator import generate_suggestions
from src.utils.file_utils import get_file_upload
from src.llm.openai import OpenAILLMFileUploadManager
from src.websockets.connection_manager import Message, MessageTypes

config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.ini"))
logging.config.fileConfig(fname=config_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    try:
        await dataset_upload()
    except Exception as e:
        logger.exception(f"Failed to populate database with initial data from file: {e}")
    yield
    # shut down
    # If running app with docker compose, Ctrl+C will detach from container immediately,
    # meaning no graceful shutdown logs will be seen
    openai_file_manager = OpenAILLMFileUploadManager()
    await openai_file_manager.delete_all_files()


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
app.add_middleware(ScratchPadMiddleware)

health_prefix = "InferESG healthcheck: "
further_guidance = "Please check the README files for further guidance."

healthy_response = health_prefix + "backend is healthy. Neo4J is healthy."
unhealthy_backend_response = health_prefix + "backend is unhealthy. Unable to healthcheck Neo4J. " + further_guidance
unhealthy_neo4j_response = health_prefix + "backend is healthy. Neo4J is unhealthy. " + further_guidance

chat_fail_response = "Unable to generate a response. Check the service by using the keyphrase 'healthcheck'"
suggestions_failed_response = "Unable to generate suggestions. Check the service by using the keyphrase 'healthcheck'"
file_upload_failed_response = "Unable to upload file. Check the service by using the keyphrase 'healthcheck'"
file_get_upload_failed_response = "Unable to get uploaded file. Check the service by using the keyphrase 'healthcheck'"
report_get_upload_failed_response = "Unable to download report. Check the service by using the keyphrase 'healthcheck'"


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


@app.delete("/chat")
async def clear_chat():
    logger.info("Delete the chat session")
    try:
        cancellation_message = Message(type=MessageTypes.REPORT_CANCELLED, data="Chat session cleared")
        await connection_manager.broadcast(cancellation_message)
        # clear chatresponses and files first as need session data for keys
        clear_chat_messages(get_session_chat_response_ids())
        clear_session_file_uploads()
        reset_session()
        return Response(status_code=204)
    except Exception as e:
        logger.exception(e)
        return Response(status_code=500)


@app.get("/chat/{id}")
def chat_message(id: str):
    logger.info(f"Get chat message called with id: {id}")
    try:
        final_result = get_chat_message(id)
        if final_result is None:
            return JSONResponse(status_code=404, content=f"Message with id {id} not found")
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


@app.post("/report")
async def report(file: UploadFile, background_tasks: BackgroundTasks):
    logger.info(f"Uploading file: {file.filename}")
    try:
        file_contents = await file.read()
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename missing from file upload.")

        existing_id = get_llm_file_upload_id(file.filename)
        if existing_id:
            logger.info(f"File {file.filename} already uploaded to OpenAI with id '{existing_id}'")

        file_id = existing_id if existing_id else str(uuid.uuid4())
        background_tasks.add_task(generate_report, file_contents, file.filename, file_id)

        return JSONResponse(
            status_code=200,
            content={"message": "File uploaded successfully", "id": file_id},
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=file_upload_failed_response)


async def generate_report(file_contents: bytes, filename: str, file_id: str ):
    try:
        logger.info(f"Generating report for file: {filename} with ID: {file_id}")
        progress_message = Message(type=MessageTypes.REPORT_IN_PROGRESS, data="Report generation started")
        await connection_manager.broadcast(progress_message)

        report_response = await create_report_from_file(file_contents, filename, file_id)

        complete_message = Message(
            type=MessageTypes.REPORT_COMPLETE,
            data=json.dumps(
                {
                    "id": file_id,
                    "filename": report_response["filename"],
                    "report": report_response["report"],
                    "answer": report_response["answer"],
                }
            ),
        )
        await connection_manager.broadcast(complete_message)
    except Exception as e:
        logger.exception(f"Error generating report: {e}")
        error_message = Message(type=MessageTypes.REPORT_FAILED, data="Report generation failed")
        await connection_manager.broadcast(error_message)

@app.get("/report/{id}")
def download_report(id: str):
    logger.info(f"Get report download called for id: {id}")
    try:
        final_result = get_report(id)
        if final_result is None:
            return JSONResponse(status_code=404, content=f"Message with id {id} not found")
        headers = {"Content-Disposition": 'attachment; filename="report.md"'}
        return Response(final_result.get("report"), headers=headers, media_type="text/markdown")
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=report_get_upload_failed_response)


@app.get("/uploadfile")
async def fetch_file(id: str):
    logger.info(f"fetch uploaded file id={id} ")
    try:
        final_result = get_file_upload(id)
        if final_result is None:
            return JSONResponse(status_code=404, content=f"Upload with id {id} not found")
        return JSONResponse(status_code=200, content=final_result)
    except Exception as e:
        logger.exception(e)
        return JSONResponse(status_code=500, content=file_get_upload_failed_response)


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
