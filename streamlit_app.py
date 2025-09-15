# streamlit_app.py
import streamlit as st
import requests

# Backend URL (update if deployed somewhere else)
BACKEND_URL = "https://assisgnment-codingninja.onrender.com"

st.set_page_config(page_title="AI Interviewer", page_icon="🤖", layout="centered")

st.title("🤖 AI Interviewer")
st.write("Chat with the AI Interviewer. Answer questions and get feedback.")

# Session state for chat history
if "session_id" not in st.session_state:
    st.session_state.session_id = "test-session"
if "history" not in st.session_state:
    st.session_state.history = [
        {
            "role": "assistant",
            "content": "👋 Hello! Welcome to your Excel mock interview. "
                       "I’ll ask you a few questions, starting from basics and moving to advanced ones. "
                       "At the end, I’ll provide a feedback report on your performance. "
                       "Are you ready to begin?"
        }
    ]

# Chat input
user_input = st.chat_input("Type your response...")
if user_input:
    # Append user input to history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Call backend
    response = requests.post(
        f"{BACKEND_URL}/v1/query",
        json={"query": user_input, "history": st.session_state.history},
    )

    if response.status_code == 200:
        bot_reply = response.json().get("response", "⚠️ No reply from backend")
        st.session_state.history.append({"role": "assistant", "content": bot_reply})
    else:
        st.error(f"Error {response.status_code}: {response.text}")

# Display conversation
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
