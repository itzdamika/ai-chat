import uvicorn
from app.chatbot_app import get_app

app = get_app()

if __name__ == "__main__":
    # Run the Uvicorn server with auto-reload enabled
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)