import datetime
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from app.session_manager import SessionManager
from app.chat_service import ChatService
from app.config import Config
from openai import AzureOpenAI
from app.logging_config import logger

router = APIRouter()

# Initialize configuration, OpenAI client, chat service, and session manager
config = Config()
openai_client = AzureOpenAI(
    api_key=config.AZURE_OPENAI_API_KEY,
    api_version=config.AZURE_OPENAI_VERSION,
    azure_endpoint=config.AZURE_ENDPOINT,
)
chat_service = ChatService(config, openai_client)
session_manager = SessionManager()

@router.post("/chat")
async def chat(request: Request):
    """
    Chat endpoint to process user messages.
    Expects JSON with 'sessionID', 'message', and optionally 'Language'.
    """
    data = await request.json()
    session_id: Optional[str] = data.get("sessionID")
    user_message: Optional[str] = data.get("message")
    language: Optional[str] = data.get("Language", "English")
    
    if not session_id or not user_message:
        raise HTTPException(status_code=400, detail="Missing 'sessionID' or 'message'")
    
    logger.info("Received chat request", session_id=session_id, language=language, user_message=user_message)
    
    session = session_manager.get_session(session_id)
    response_text = await chat_service.process_message(session, user_message, language)
    return {"response": response_text}

@router.get("/health")
async def health_check():
    """
    Health check endpoint to confirm the API is running.
    """
    return {"status": "OK", "timestamp": datetime.datetime.utcnow().isoformat()}
