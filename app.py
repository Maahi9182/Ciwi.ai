import os
import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="Ciwi AI",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom High-Contrast & Glassmorphic Styling
st.markdown(
    """
    <style>
    /* Dark background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171923 0%, #0d1117 100%);
        color: #F8FAFC;
    }

    /* Crisp white text for readability */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    p, span, div, li {
        color: #E2E8F0 !important;
        font-size: 1.02rem;
        line-height: 1.65;
    }

    /* Glass chat bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 1.1rem 1.4rem !important;
        margin-bottom: 0.9rem !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    /* Subdued purple highlight on Ciwi messages */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(99, 102, 241, 0.08) !important;
        border: 1px solid rgba(129, 140, 248, 0.25) !important;
    }

    /* Glass floating input bar */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    [data-testid="stChatInput"] {
        background: rgba(15, 23, 42, 0.65) !important;
        backdrop-filter: blur(20px) saturate(190%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(190%) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(129, 140, 248, 0.7) !important;
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.25) !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94A3B8 !important;
    }

    /* Header styling */
    .app-header {
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 30%, #818CF8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #94A3B8 !important;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Title
st.markdown(
    """
    <div class="app-header">
        <div class="app-title">✨ Ciwi AI</div>
        <div class="app-subtitle">Intelligent • Authentic • Grounded</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# API client initialization
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("Please add your GEMINI_API_KEY in the app settings.")
    st.stop()

client = genai.Client(api_key=api_key)

# Session history initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": [
                {
                    "text": "Hello! I am Ciwi, your AI assistant. What would you like to explore or build today?"
                }
            ],
        }
    ]

# Render chat messages
for msg in st.session_state.messages:
    role = "assistant" if msg["role"] == "model" else "user"
    avatar = "✨" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["parts"][0]["text"])

# Handle interaction
if prompt := st.chat_input("Ask Ciwi anything..."):
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

    with st.chat_message("assistant", avatar="✨"):
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=st.session_state.messages,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are Ciwi, an authentic, adaptive, and grounded AI collaborator with a touch of wit. "
                    "Format responses with clear hierarchy, high readability, and clean Markdown structure."
                ),
                temperature=0.7,
            ),
        )
        st.markdown(response.text)
        st.session_state.messages.append(
            {"role": "model", "parts": [{"text": response.text}]}
        )
