import streamlit as st
import requests
import random
import string

def generate_session_id(length: int = 25) -> str:
    """
    Generate a random alphanumeric session ID of the given length.
    
    Args:
        length (int): Length of the session ID (default is 25).
        
    Returns:
        str: A random session ID.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_backend_response(session_id: str, user_message: str, language: str) -> str:
    """
    Send a POST request to the chatbot backend and return the assistant's response.
    
    Args:
        session_id (str): Unique session identifier.
        user_message (str): User's message.
        language (str): Selected language for the response.
    
    Returns:
        str: Response text from the backend or an error message.
    """
    backend_url = "http://127.0.0.1:5000/chat"
    payload = {
        "sessionID": session_id,
        "message": user_message,
        "Language": language,
    }
    try:
        response = requests.post(backend_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from the server.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"

def initialize_session_state() -> None:
    """
    Initialize session state variables if not already set.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "English"

def display_chat_history() -> None:
    """
    Display the chat history using Streamlit's chat message components.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main() -> None:
    """
    Main function to run the Streamlit chatbot frontend.
    """
    st.set_page_config(page_title="Chatbot Assistant", layout="wide")
    st.title("Chatbot Assistant")

    # Initialize session state variables
    initialize_session_state()
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        languages = ["English", "Spanish", "French", "German", "Chinese"]
        st.session_state.selected_language = st.selectbox("Select Language", languages, index=languages.index(st.session_state.selected_language))

    # Display session ID for reference
    st.write(f"**Session ID:** {st.session_state.session_id}")
    
    # Display previous chat history
    display_chat_history()
    
    # Get user input via chat input
    user_message = st.chat_input("Type your message here...")
    if user_message:
        # Append user message to session state and display it
        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)
        
        # Display a placeholder for the assistant's response
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")

            # Retrieve the assistant's response from the backend
            bot_response = get_backend_response(
                st.session_state.session_id,
                user_message,
                st.session_state.selected_language
            )
            
            # Update placeholder with the actual response
            placeholder.markdown(bot_response)
        
        # Save the assistant's response in session state
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    main()
