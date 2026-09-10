import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Page Configuration & Aesthetics
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ciwi AI — Intelligence Refined",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom High-End Styling (Dark luxury theme, modern typography & custom chat cards)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Global Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #171b26 0%, #0b0d13 100%);
        color: #f1f5f9;
    }

    /* Header Styling */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px 0 25px 0;
        text-align: center;
    }

    .brand-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-radius: 999px;
        padding: 6px 16px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #a5b4fc;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.15);
    }

    .brand-title {
        font-size: 2.75rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .brand-subtitle {
        font-size: 0.98rem;
        color: #64748b;
        margin-top: 8px;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(22, 27, 39, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 18px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    }

    /* User Message Differentiation */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        background: rgba(30, 41, 59, 0.55) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
    }

    /* Text Typography inside chat */
    [data-testid="stChatMessage"] p {
        color: #e2e8f0;
        font-size: 0.98rem;
        line-height: 1.65;
        font-weight: 400;
    }

    /* Input Box Redesign */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        background-color: rgba(18, 22, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        transition: all 0.2s ease-in-out;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.3) !important;
    }

    /* Hide standard Streamlit header & toolbar */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    #MainMenu, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Visual Header
# ---------------------------------------------------------
st.markdown(
    """
    <div class="header-container">
        <div class="brand-badge">
            <span style="font-size: 1rem;">✦</span> PRO AGENT ENGINE
        </div>
        <h1 class="brand-title">Ciwi AI</h1>
        <p class="brand-subtitle">High-performance intelligence, reasoning & workflows</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# API Client & Secrets Initialization
# ---------------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

if not api_key:
    st.error("Missing GEMINI_API_KEY. Please set it in your Streamlit Secrets or Environment Variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# Premium Custom Avatars
# ---------------------------------------------------------
CIWI_AVATAR = "https://api.iconify.design/solar:atom-bold-duotone.svg?color=%23818cf8"
USER_AVATAR = "https://api.iconify.design/solar:user-circle-bold-duotone.svg?color=%2338bdf8"

# ---------------------------------------------------------
# Chat Session Management
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": [
                {
                    "text": "Greetings! I am **Ciwi**, your AI assistant. How can we elevate your work today?"
                }
            ],
        }
    ]

# Render Message History
for msg in st.session_state.messages:
    if msg["role"] == "model":
        with st.chat_message("assistant", avatar=CIWI_AVATAR):
            st.markdown(msg["parts"][0]["text"])
    else:
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(msg["parts"][0]["text"])

# ---------------------------------------------------------
# Prompt Execution
# ---------------------------------------------------------
if prompt := st.chat_input("Ask Ciwi anything..."):
    # Render user input
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

    # Generate assistant reply with Ciwi persona
    with st.chat_message("assistant", avatar=CIWI_AVATAR):
        with st.spinner("Ciwi is synthesizing..."):
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=st.session_state.messages,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Ciwi, an elite, polished AI strategist and collaborator. "
                        "You provide precise, articulate, and well-structured responses. "
                        "Always identify yourself as Ciwi when asked."
                    ),
                    temperature=0.7,
                ),
            )
            st.markdown(response.text)
            st.session_state.messages.append(
                {"role": "model", "parts": [{"text": response.text}]}
            )
