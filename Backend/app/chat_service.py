import asyncio
from typing import Any, Dict

from openai import AzureOpenAI
from prompts import chat_prompt
from app.conversation import ConversationGraph
from app.config import Config
from app.logging_config import logger

class ChatService:
    """
    Processes user messages using Azure OpenAI.
    Manages context extraction and API calls for chat completions.
    """
    def __init__(self, config: Config, openai_client: AzureOpenAI) -> None:
        self.config = config
        self.openai_client = openai_client

    async def _create_completion(self, messages: list, **kwargs) -> str:
        """
        Calls the OpenAI API in a separate thread with default parameters.
        """
        default_kwargs = {
            "model": self.config.AZURE_OPENAI_DEPLOYMENT_ID,
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.95,
        }
        default_kwargs.update(kwargs)
        response = await asyncio.to_thread(
            lambda: self.openai_client.chat.completions.create(
                messages=messages, **default_kwargs
            )
        )
        return response.choices[0].message.content.strip()

    async def handle_user_query(self, session: Dict[str, Any], user_message: str, language: str) -> str:
        """
        Constructs messages (including context) and retrieves the generated response.
        """
        conversation_graph: ConversationGraph = session["conversation_graph"]
        context = conversation_graph.get_relevant_context(user_message)
        
        messages = [
            {"role": "system", "content": chat_prompt},
            {"role": "user", "content": f"Current Question: {user_message}"},
            {"role": "system", "content": f"Respond exclusively in: {language}."},
            {"role": "user", "content": f"Conversation context: {context}"}
        ]
        return await self._create_completion(messages)

    async def process_message(self, session: Dict[str, Any], user_message: str, language: str) -> str:
        """
        Processes the user message, updates the conversation graph,
        and returns the assistant's response.
        """
        try:
            if "conversation_graph" not in session:
                session["conversation_graph"] = ConversationGraph()
            conversation_graph: ConversationGraph = session["conversation_graph"]
            
            session["message_count"] = session.get("message_count", 0) + 1
            conversation_graph.add_message(user_message, "user")
            
            response_text = await self.handle_user_query(session, user_message, language)
            conversation_graph.add_message(response_text, "assistant")
            return response_text
        except Exception as e:
            logger.error("Error in process_message", error=str(e))
            fallback = "I'm sorry, I did not understand your request"
            if "conversation_graph" in session:
                session["conversation_graph"].add_message(fallback, "assistant")
            return fallback