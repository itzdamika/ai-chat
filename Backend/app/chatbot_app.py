from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import logger
from app.routes import router

class ChatbotApp:
    """
    Encapsulates the FastAPI application setup.
    Configures middleware, routes, and graceful shutdown events.
    """
    def __init__(self) -> None:
        self.app = FastAPI(
            title="AI Chatbot API",
            description="API for an AI-powered chatbot using Azure OpenAI, FastAPI, and advanced conversation management.",
            version="1.0.0"
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app.include_router(router)
        self.add_shutdown_event()

    def add_shutdown_event(self) -> None:
        """
        Registers a shutdown event handler for cleanup.
        """
        @self.app.on_event("shutdown")
        async def shutdown_event():
            logger.info("Shutting down Chatbot API...")

def get_app() -> FastAPI:
    """
    Returns the configured FastAPI application.
    """
    chatbot_app = ChatbotApp()
    return chatbot_app.app
