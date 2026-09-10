import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Ciwi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Full Dark Canvas & Replit Amber Glow */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        background-image: radial-gradient(ellipse 65% 38% at 50% 88%, rgba(155, 52, 18, 0.28) 0%, rgba(14, 17, 23, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 880px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1C222E !important;
        padding-top: 0.8rem !important;
    }

    .sb-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.4rem 1rem 0.4rem;
    }

    .workspace-pill {
        background: #181E28;
        border: 1px solid #232B39;
        border-radius: 8px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #F1F5F9;
        font-size: 0.86rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    .new-btn {
        background: #1B212D;
        border: 1px solid #283344;
        border-radius: 8px;
        padding: 7px 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.88rem;
        margin-bottom: 0.8rem;
    }

    .sb-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 7px 10px;
        border-radius: 6px;
        font-size: 0.86rem;
        color: #94A3B8;
        cursor: pointer;
    }

    .sb-item:hover {
        background-color: #181E29;
        color: #FFFFFF;
    }

    .upgrade-box {
        background: #151A24;
        border: 1px solid #232B39;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.5rem;
    }

    .progress-bar-bg {
        background: #232B39;
        border-radius: 999px;
        height: 4px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }

    .progress-bar-fill {
        background: #0070F3;
        height: 100%;
        width: 100%;
    }

    /* Top Recent Cards */
    .recent-card {
        background: #131722;
        border: 1px solid #202736;
        border-radius: 12px;
        padding: 0.85rem 1.1rem;
        cursor: pointer;
    }

    /* Stacked Pill Buttons */
    div.stButton > button {
        background-color: #161A23 !important;
        color: #D1D5DB !important;
        border: 1px solid #262E3D !important;
        border-radius: 9999px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1.1rem !important;
        display: inline-flex !important;
        align-items: center !important;
        margin-bottom: 0.3rem !important;
    }

    div.stButton > button:hover {
        background-color: #212836 !important;
        border-color: #38455B !important;
        color: #FFFFFF !important;
    }

    /* Credit Warning Banner */
    .credit-banner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 2.2rem;
        margin-bottom: 0.8rem;
        font-size: 0.86rem;
        color: #94A3B8;
    }

    .btn-upgrade-core {
        background: #0070F3;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 6px 14px;
        font-size: 0.84rem;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Replit Custom Input Console */
    [data-testid="stForm"] {
        background-color: #141822 !important;
        border: 1px solid #262E3E !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem 0.65rem 1.1rem !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5) !important;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #3B475C !important;
    }

    [data-testid="stForm"] div[data-testid="stTextInput"],
    [data-testid="stForm"] div[data-testid="stTextInputRootElement"],
    [data-testid="stForm"] div[data-baseweb="input"],
    [data-testid="stForm"] div[data-baseweb="base-input"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        padding: 0 !important;
    }

    /* Ensure user typed text is clearly visible */
    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        color: #FFFFFF !important;
        padding: 0.1rem 0 1rem 0 !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #64748B !important;
    }

    .console-bottom-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #1C2330;
        padding-top: 0.5rem;
    }

    /* Replit Arrow Submit Button */
    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: transparent !important;
        border: none !important;
        color: #7E8B9D !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 0 !important;
        min-width: 24px !important;
        width: 24px !important;
        height: 24px !important;
        box-shadow: none !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        color: #FFFFFF !important;
    }

    /* Chat Messages styling */
    [data-testid="stChatMessage"] {
        background-color: #141822 !important;
        border: 1px solid #232B3A !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    [data-testid="stChatMessage"] * {
        color: #E6EDF3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# State initialization
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "html_code" not in st.session_state:
    st.session_state.html_code = ""

def is_design_task(text: str) -> bool:
    keywords = ["build", "create", "make a website", "make an app", "design", "redesign", "add button", "clone", "dashboard", "html", "css"]
    return any(k in text.lower() for k in keywords)

def query_gemini(prompt: str, is_design: bool):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Missing GEMINI_API_KEY in Secrets."
    client = genai.Client(api_key=api_key)

    if is_design:
        sys_prompt = (
            "You are Ciwi, an elite autonomous web-building AI. "
            "1. Give a concise summary of changes in bullet points. "
            "2. Provide complete, responsive standalone HTML/CSS/JS inside a ```html
