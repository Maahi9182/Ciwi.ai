import os
import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="Ciwi AI", page_icon="🤖")
st.title("🤖 Ciwi AI Assistant")

# Retrieve API key securely from Streamlit secrets or environment
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("Please provide a GEMINI_API_KEY in secrets or environment.")
    st.stop()

client = genai.Client(api_key=api_key)

# Initialize session history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": [{"text": "Hello! I am Ciwi, your AI assistant. How can I help you today?"}]}
    ]

# Display existing chat messages
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(msg["parts"][0]["text"])

# Handle user input
if prompt := st.chat_input("Ask Ciwi anything..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=st.session_state.messages,
            config=types.GenerateContentConfig(
                system_instruction="You are Ciwi, an intelligent, authentic, and grounded AI collaborator. Introduce yourself as Ciwi.",
                temperature=0.7,
            )
        )
        st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "parts": [{"text": response.text}]})
