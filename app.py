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
    /* Global Obsidian Theme */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        background-image: radial-gradient(ellipse 65% 38% at 50% 90%, rgba(155, 52, 18, 0.25) 0%, rgba(14, 17, 23, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Fixed Layout & Bottom Anchor */
    .main .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
        padding-bottom: 7rem !important;
        margin: 0 auto !important;
    }

    .workspace-active .main .block-container {
        max-width: 100% !important;
        padding: 1rem 1.5rem 7rem 1.5rem !important;
    }

    /* Sidebar Styling */
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

    /* Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #161A23 !important;
        border: 1px solid #242B38 !important;
        border-radius: 12px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.9rem !important;
    }

    [data-testid="stChatMessage"] * {
        color: #F3F4F6 !important;
        line-height: 1.6 !important;
    }

    /* Pinned Bottom Input */
    [data-testid="stBottomBlockContainer"] {
        background-color: #0E1117 !important;
        border-top: 1px solid #1C222E !important;
        padding: 0.8rem 1rem !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #161A23 !important;
        border: 1px solid #283344 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.45) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    /* Clean Category Action Pills */
    div.stButton > button {
        background-color: #181D26 !important;
        color: #D1D5DB !important;
        border: 1px solid #2A3344 !important;
        border-radius: 9999px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1rem !important;
        display: inline-flex !important;
        align-items: center !important;
        margin-bottom: 0.35rem !important;
    }

    div.stButton > button:hover {
        background-color: #222936 !important;
        border-color: #3F4C62 !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session State
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "project_name" not in st.session_state:
    st.session_state.project_name = "Ciwi AI Assistant"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "chat"  # 'chat' or 'build_slide'
if "messages" not in st.session_state:
    st.session_state.messages = []
if "html_code" not in st.session_state:
    st.session_state.html_code = ""

def detect_build_intent(prompt: str) -> bool:
    """Detects if prompt requests creating a website, app, UI, or design component."""
    keywords = ["build", "create", "make a website", "make an app", "design", "redesign", "add button", "clone", "code", "html", "css"]
    return any(k in prompt.lower() for k in keywords)

def query_gemini(prompt: str, is_build: bool):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Please add your GEMINI_API_KEY to Streamlit Secrets."
    
    client = genai.Client(api_key=api_key)

    if is_build:
        sys_inst = (
            "You are Ciwi, an elite autonomous web-building AI. "
            "1. Give a concise summary of changes and color scheme in markdown. "
            "2. Provide complete, fully functional standalone HTML/CSS/JS inside a ```html ``` block."
        )
        context = f"Current App Code:\n{st.session_state.html_code}\n\nUser request: {prompt}"
    else:
        sys_inst = (
            "You are Ciwi, a helpful and sharp AI assistant. "
            "Provide clean, direct conversational replies. "
            "Do NOT write HTML apps, UI cards, or code blocks for general chat or greetings."
        )
        context = prompt

    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=context,
        config=types.GenerateContentConfig(system_instruction=sys_inst, temperature=0.7),
    )
    return res.text

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div class="sb-header">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522"><path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/></svg>
            <div style="display:flex; gap:12px; color:#8B949E; font-size: 0.95rem;">
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

        <div class="new-btn">
            <span>+</span>
            <span>New</span>
        </div>

        <div class="sb-item"><span>📥</span> <span>Import</span></div>
        <div class="sb-item"><span>📁</span> <span>Projects</span></div>
        <div class="sb-item">
            <span>⏱️</span> <span>Routines</span> 
            <span style="background:#19273D; color:#38BDF8; font-size:0.68rem; font-weight:700; padding:1px 6px; border-radius:4px; margin-left:auto;">Beta</span>
        </div>
        <div class="sb-item"><span>📚</span> <span>Library</span></div>
        <div class="sb-item"><span>🔌</span> <span>Integrations</span></div>
        <div class="sb-item"><span>🛡️</span> <span>Security</span></div>

        <div style="font-size:0.74rem; font-weight:700; color:#64748B; padding:1.2rem 0.4rem 0.3rem 0.4rem;">Recent</div>
        <div class="sb-item"><span>🗂️</span> <span>Ciwi AI Assistant</span></div>
        <div class="sb-item"><span>🗂️</span> <span>Fashion Showcase</span></div>
        <div class="sb-item"><span>🗂️</span> <span>Dine Easy</span></div>

        <div class="upgrade-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
                    <div style="font-size:0.72rem; color:#8B949E; margin-top:2px;">Unlock more credits</div>
                </div>
                <div style="background:#0070F3; border-radius:6px; width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#FFF; font-weight:700;">+</div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#8B949E; margin-top:8px;">
                <span>Free allowance</span>
                <span>100% used</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
        </div>

        <div style="margin-top:1.2rem;">
            <div class="sb-item"><span>❔</span> <span>Learn more</span></div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; padding:0.8rem 0.4rem 0.2rem 0.4rem; margin-top:0.8rem; border-top:1px solid #1C222E;">
            <div style="display:flex; align-items:center; gap:8px; color:#FFFFFF; font-weight:600; font-size:0.88rem;">
                <span>👤</span>
                <span>Mahesh</span>
            </div>
            <span style="color:#64748B; cursor:pointer;">⚙️</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- MODE 1: Standard Chat View (Normal conversation & questions) ---
if st.session_state.view_mode == "chat":
    # Top hero greeting if chat is fresh
    if not st.session_state.messages:
        st.markdown(
            f'<div style="font-size:2.5rem; font-weight:600; color:#F3F4F6; margin-bottom:1.4rem;">{st.session_state.user_name}, what are we working on today?</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:6px; font-size:0.8rem; color:#8C96A5; margin-bottom:0.75rem;">
                <span>Choose action or start typing</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Clear distinct category pills
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            if st.button("🌐  Website Builder", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "Build a modern responsive website"})
                st.session_state.view_mode = "build_slide"
                reply = query_gemini("Build a modern responsive landing page website", is_build=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                st.rerun()

        with col_c2:
            if st.button("📱  Mobile App View", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "Build a mobile app layout"})
                st.session_state.view_mode = "build_slide"
                reply = query_gemini("Build a mobile app interface with navigation and cards", is_build=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                st.rerun()

        with col_c3:
            if st.button("🎨  UI Component Design", use_container_width=True):
                st.session_state.messages.append({"role": "user", "text": "Build an interactive UI component"})
                st.session_state.view_mode = "build_slide"
                reply = query_gemini("Build an interactive dashboard component", is_build=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                st.rerun()

    # Chat history display (pops up above the bottom bar)
    for m in st.session_state.messages:
        role = "assistant" if m["role"] == "model" else "user"
        with st.chat_message(role):
            st.markdown(m["text"])

    # Bottom pinned input
    if prompt_text := st.chat_input("Start chatting or describe a task..."):
        st.session_state.messages.append({"role": "user", "text": prompt_text})
        is_build = detect_build_intent(prompt_text)

        if is_build:
            st.session_state.view_mode = "build_slide"
            with st.spinner("⚡ Ciwi Agent launching build workspace..."):
                reply = query_gemini(prompt_text, is_build=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                else:
                    st.session_state.messages.append({"role": "model", "text": reply})
        else:
            with st.spinner("⚡ Ciwi responding..."):
                reply = query_gemini(prompt_text, is_build=False)
                st.session_state.messages.append({"role": "model", "text": reply})

        st.rerun()

# --- MODE 2: Build Workspace (Split slide with live interactive preview) ---
else:
    t_left, t_right = st.columns([7, 3])
    with t_left:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:12px; margin-bottom: 0.6rem;">
                <span style="background:#181E28; border:1px solid #232B39; padding:4px 10px; border-radius:6px; font-weight:700; font-size:0.85rem; color:#FFF;">📁 {st.session_state.project_name} ▾</span>
                <span style="color:#94A3B8; font-size:0.82rem; font-weight:600;">Design</span>
                <span style="color:#F26522; font-size:0.82rem; font-weight:700; border-bottom:2px solid #F26522;">Build</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with t_right:
        if st.button("← Back to Chat", use_container_width=True):
            st.session_state.view_mode = "chat"
            st.rerun()

    c_chat, c_prev = st.columns([1, 1], gap="medium")

    with c_chat:
        chat_box = st.container(height=520)
        with chat_box:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["text"])

        if sub_msg := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "text": sub_msg})
            with st.spinner("⚡ Updating live build..."):
                reply = query_gemini(sub_msg, is_build=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                else:
                    st.session_state.messages.append({"role": "model", "text": reply})
            st.rerun()

    with c_prev:
        st.markdown(
            """
            <div style="background:#161B24; border:1px solid #262E3E; border-radius:12px 12px 0 0; padding:0.5rem 0.8rem; display:flex; align-items:center; gap:8px;">
                <span style="background:#0E1117; border:1px solid #262E3E; border-radius:6px; padding:2px 8px; font-size:0.75rem; color:#CBD5E1;">Ciwi Live Preview ✕</span>
                <div style="background:#0E1117; border:1px solid #262E3E; border-radius:6px; padding:2px 8px; font-size:0.75rem; color:#8B949E; flex-grow:1; font-family:monospace;">
                    https://ciwi.replit.dev/live-preview
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        components.html(st.session_state.html_code, height=520, scrolling=True)
