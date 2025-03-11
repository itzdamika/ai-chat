# Chatbot Assistant

Chatbot Assistant is an AI-powered chatbot application built using **FastAPI** for the backend and **Streamlit** for the frontend. It integrates **Azure OpenAI** for natural language processing and supports multi-session conversations with a graph-based conversation context manager.

---

## Features

- **FastAPI Backend**: Handles chat requests, manages sessions, and communicates with Azure OpenAI.
- **Streamlit Frontend**: Provides an interactive UI for users to chat with the assistant.
- **Session Management**: Uses a unique session ID to maintain chat history.
- **Multi-Language Support**: Users can select their preferred response language.
- **Logging & Debugging**: Logs requests and responses for analysis and debugging.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **pip (Python Package Manager)**
- **Virtual Environment (optional but recommended)**

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/itzdamika/ai-chat.git
cd ai-chat
```

### 2. Create and Activate a Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r Backend/requirements.txt
pip install -r Frontend/requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file inside the `Backend/` directory and add the following:

```
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_ID=your-deployment-id
AZURE_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_VERSION=your-api-version
```

Replace `your-api-key-here`, `your-deployment-id`, and `your-azure-endpoint` with your actual Azure OpenAI credentials.

---

## Running the Application

### 1. Start the Backend Server

Navigate to the **Backend** directory and run:
```bash
cd Backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

The backend will now be running at `http://127.0.0.1:5000`.

### 2. Start the Frontend

Open a new terminal window, navigate to the **Frontend** directory, and run:
```bash
cd Frontend
streamlit run frontend.py
```

This will start the chatbot UI in your web browser.

---

## Usage

1. Open the **Streamlit UI** in your browser (the link will appear in the terminal).
2. Type your message in the input box and select your preferred language from the dropdown.
3. The assistant will respond based on the conversation context.

---

## Project Structure

```
chatbot-assistant/
├── Backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── chat_service.py
│   │   ├── chatbot_app.py
│   │   ├── config.py
│   │   ├── conversation.py
│   │   ├── logging_config.py
│   │   ├── routes.py
│   │   ├── session_manager.py
│   ├── .env
│   ├── main.py
│   ├── prompts.py
│   ├── requirements.txt
├── Frontend/
│   ├── frontend.py
│   ├── requirements.txt
├── README.md
```

---

## API Endpoints

### 1. Chat Endpoint
- **URL**: `/chat`
- **Method**: `POST`
- **Request Body (JSON Format)**:

```json
{
  "sessionID": "your-session-id",
  "message": "Hello, chatbot!",
  "Language": "English"
}
```

- **Response Example**:

```json
{
  "response": "Hello! How can I assist you today?"
}
```

### 2. Health Check Endpoint
- **URL**: `/health`
- **Method**: `GET`
- **Response Example**:

```json
{
  "status": "OK",
  "timestamp": "2025-03-11T12:00:00Z"
}
```

---

## Troubleshooting

**1. Backend not starting?**
- Ensure that your `.env` file is correctly set up.
- Check if **Azure OpenAI API Key** is valid.
- Make sure all dependencies are installed (`pip install -r Backend/requirements.txt`).

**2. Frontend not opening?**
- Make sure the backend is running before launching the frontend.
- Ensure you’re using the correct Python environment.

**3. Getting a 500 error?**
- Check the backend logs for more details (`logs/app.log`).

---

## License
This project is licensed under the **MIT License**. You are free to modify and distribute the code with attribution.

---

## Contributors
Feel free to contribute to this project by submitting **pull requests** or reporting **issues**.

---

## Contact
For any inquiries or support, reach out via **damikaudantha@gmail.com** or open an issue in the GitHub repository.

---

