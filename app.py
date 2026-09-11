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

# ---------------------------------------------------------
# Warm Beige & Orange Theme Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Warm Beige Canvas */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #FBF8F3 !important;
        background-image: radial-gradient(ellipse 70% 45% at 50% 92%, rgba(242, 101, 34, 0.12) 0%, rgba(251, 248, 243, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #1F2937 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 1080px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        margin: 0 auto !important;
    }

    /* Left Sidebar: Warm Off-White / Light Cream */
    [data-testid="stSidebar"] {
        background-color: #F5EFEB !important;
        border-right: 1px solid #E5DCD0 !important;
        padding-top: 0.6rem !important;
    }

    .sb-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.4rem 0.8rem 0.4rem;
    }

    .workspace-pill {
        background: #ECE3D8;
        border: 1px solid #DFD4C5;
        border-radius: 8px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #2D3748;
        font-size: 0.86rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    /* Sidebar Buttons */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #4B5563 !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.4rem 0.6rem !important;
        width: 100% !important;
        box-shadow: none !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #ECE3D8 !important;
        color: #111827 !important;
    }

    .upgrade-box {
        background: #EDE4D8;
        border: 1px solid #DFD4C5;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.2rem;
    }

    .progress-bar-bg {
        background: #DFD4C5;
        border-radius: 999px;
        height: 4px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }

    .progress-bar-fill {
        background: #F26522;
        height: 100%;
        width: 100%;
    }

    /* Warm Cards */
    .import-card {
        background: #FFFFFF;
        border: 1px solid #E8DFD3;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        transition: border-color 0.15s, transform 0.15s;
    }

    .import-card:hover {
        border-color: #F26522;
        transform: translateY(-1px);
    }

    .project-preview-card {
        background: #FFFFFF;
        border: 1px solid #E8DFD3;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .preview-thumb {
        height: 140px;
        background: #F7F2EA;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid #E8DFD3;
        font-size: 2rem;
    }

    .preview-footer {
        padding: 0.9rem 1.1rem;
    }

    /* Pill Buttons on Dashboard */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5DCD0 !important;
        border-radius: 9999px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1.1rem !important;
        display: inline-flex !important;
        align-items: center !important;
        margin-bottom: 0.3rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    div.stButton > button:hover {
        background-color: #FFFDF9 !important;
        border-color: #F26522 !important;
        color: #F26522 !important;
    }

    /* Replit Input Console in Warm Beige / Crisp White */
    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E8DFD3 !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem 0.65rem 1.1rem !important;
        box-shadow: 0 8px 24px rgba(242, 101, 34, 0.06) !important;
        position: relative !important;
        margin-top: 0.6rem !important;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #F26522 !important;
        box-shadow: 0 8px 28px rgba(242, 101, 34, 0.14) !important;
    }

    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        color: #1F2937 !important;
        padding: 0.1rem 0 1rem 0 !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #9CA3AF !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: #F26522 !important;
        border: none !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0 !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        position: absolute !important;
        right: 1.1rem !important;
        bottom: 0.65rem !important;
        z-index: 10 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 6px rgba(242, 101, 34, 0.3) !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background: #DC5416 !important;
        transform: scale(1.05);
    }

    .console-bottom-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #F3ECE1;
        padding-top: 0.5rem;
    }

    /* Chat Messages: Crisp White Card on Beige */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD3 !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }

    [data-testid="stChatMessage"] * {
        color: #1F2937 !important;
    }

    /* Orange Upgrade Button */
    .btn-upgrade-orange {
        background: #F26522;
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
        box-shadow: 0 2px 8px rgba(242, 101, 34, 0.25);
    }

    .btn-upgrade-orange:hover {
        background: #DC5416;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Initializations
# ---------------------------------------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "current_nav" not in st.session_state:
    st.session_state.current_nav = "Home"
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
            "You are Ciwi, an autonomous web-building AI. "
            "1. Give a concise summary of changes in bullet points. "
            "2. Provide complete standalone HTML/CSS/JS inside a ```html block."
        )
        context = f"Current App Code:\n{st.session_state.html_code}\n\nTask: {prompt}"
    else:
        sys_prompt = "You are Ciwi, a helpful AI assistant. Provide concise, friendly conversation. Do NOT output code or HTML."
        context = prompt

    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=context,
        config=types.GenerateContentConfig(system_instruction=sys_prompt, temperature=0.7),
    )
    return res.text

# ---------------------------------------------------------
# Left Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sb-header">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522"><path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/></svg>
            <div style="display:flex; gap:12px; color:#6B7280; font-size: 0.95rem;">
                <span>🔍</span>
                <span>◫</span>
            </div>
        </div>
        <div class="workspace-pill">
            <div style="display:flex; align-items:center; gap:8px;">
                <span>👤</span>
                <span>Personal workspace</span>
            </div>
            <span>▾</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("➕  New", key="nav_new"):
        st.session_state.current_nav = "Home"
        st.session_state.messages = []
        st.rerun()

    if st.button("📥  Import", key="nav_import"):
        st.session_state.current_nav = "Import"
        st.rerun()

    if st.button("📁  Projects", key="nav_projects"):
        st.session_state.current_nav = "Projects"
        st.rerun()

    if st.button("⏱️  Routines  (Beta)", key="nav_routines"):
        st.session_state.current_nav = "Routines"
        st.rerun()

    if st.button("📚  Library", key="nav_library"):
        st.session_state.current_nav = "Library"
        st.rerun()

    if st.button("🔌  Integrations", key="nav_integrations"):
        st.session_state.current_nav = "Integrations"
        st.rerun()

    if st.button("🛡️  Security", key="nav_security"):
        st.session_state.current_nav = "Security"
        st.rerun()

    st.markdown("<div style='font-size:0.74rem; font-weight:700; color:#8C7B6B; padding:1.2rem 0.4rem 0.3rem 0.4rem;'>Recent</div>", unsafe_allow_html=True)
    if st.button("🗂️  Ciwi AI Assistant", key="rec_ciwi"):
        st.session_state.current_nav = "Home"
        st.rerun()
    if st.button("🗂️  Fashion Showcase", key="rec_fashion"):
        st.session_state.current_nav = "Home"
        st.rerun()
    if st.button("🗂️  Dine Easy", key="rec_dine"):
        st.session_state.current_nav = "Home"
        st.rerun()

    st.markdown(
        """
        <div class="upgrade-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.84rem; font-weight:700; color:#1F2937;">Upgrade your plan</div>
                    <div style="font-size:0.72rem; color:#6B7280; margin-top:2px;">Unlock more credits</div>
                </div>
                <div style="background:#F26522; border-radius:6px; width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#FFF; font-weight:700;">+</div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#6B7280; margin-top:8px;">
                <span>Free allowance</span>
                <span>100% used</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:1.2rem 0.4rem 0.2rem 0.4rem; border-top:1px solid #E5DCD0; margin-top:1.2rem;">
            <div style="display:flex; align-items:center; gap:8px; color:#1F2937; font-weight:600; font-size:0.88rem;">
                <span>👤</span>
                <span>Mahesh</span>
            </div>
            <span style="color:#8C7B6B; cursor:pointer;">⚙️</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECTION 1: HOME (Dashboard + Search Bar + Chat)
# ---------------------------------------------------------
if st.session_state.current_nav == "Home":
    clicked_task = None

    if not st.session_state.messages:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#6B7280; margin-bottom:0.75rem;">Recent projects</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1:
            st.
