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

# --- CSS Styling ---
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
        position: relative !important;
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

    /* Submit arrow button aligned in bottom right */
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
        position: absolute !important;
        right: 1.2rem !important;
        bottom: 0.75rem !important;
        z-index: 10 !important;
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

# Session State Initialization
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "html_code" not in st.session_state:
    st.session_state.html_code = ""

def is_design_task(text: str) -> bool:
    keywords = [
        "build", "create", "make a website", "make an app",
        "design", "redesign", "add button", "clone",
        "dashboard", "html", "css"
    ]
    return any(k in text.lower() for k in keywords)

def query_gemini(prompt: str, is_design: bool):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Missing GEMINI_API_KEY in Secrets."
    client = genai.Client(api_key=api_key)

    if is_design:
        sys_prompt = (
            "You are Ciwi, an elite autonomous web-building AI.\n"
            "1. Give a concise summary of changes in bullet points.\n"
            "2. Provide complete, responsive standalone HTML/CSS/JS inside a ```html block."
        )
        context = f"Current App Code:\n{st.session_state.html_code}\n\nTask: {prompt}"
    else:
        sys_prompt = (
            "You are Ciwi, a helpful AI assistant. "
            "Provide concise, friendly conversation. Do NOT output code or HTML."
        )
        context = prompt

    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=context,
        config=types.GenerateContentConfig(
            system_instruction=sys_prompt,
            temperature=0.7,
        ),
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

# --- View Routing ---
if st.session_state.view_mode == "home":
    st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#8B949E; margin-bottom:0.75rem;">Recent projects</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(
            """
            <div class="recent-card">
                <div style="font-size:0.92rem; font-weight:600; color:#FFFFFF;">Ciwi AI Assistant</div>
                <div style="font-size:0.76rem; color:#64748B; margin-top:4px;">🔒 · 2 minutes ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            """
            <div class="recent-card">
                <div style="font-size:0.92rem; font-weight:600; color:#FFFFFF;">Fashion Showcase</div>
                <div style="font-size:0.76rem; color:#64748B; margin-top:4px;">🔒 · 53 minutes ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            """
            <div class="recent-card">
                <div style="font-size:0.92rem; font-weight:600; color:#FFFFFF;">Dine Easy</div>
                <div style="font-size:0.76rem; color:#64748B; margin-top:4px;">🔒 · 3 months ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        f'<div style="font-size:2.5rem; font-weight:600; color:#F3F4F6; margin-bottom:1.4rem;">{st.session_state.user_name}, what are we working on today?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:6px; font-size:0.8rem; color:#8C96A5; margin-bottom:0.75rem;">
            <span>Suggested for you</span>
            <span style="cursor:pointer;">⟳</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    clicked_task = None
    if st.button("✦  Help me get things done", key="p_help"):
        clicked_task = "Build a productivity dashboard with task organization"
    if st.button("🟥  Review RevenueCat growth", key="p_rc"):
        clicked_task = "Build an analytics dashboard tracking RevenueCat MRR and subscribers"
    if st.button("📄  Turn my notes into a slide deck", key="p_deck"):
        clicked_task = "Build a presentation slide generator app from user notes"

    st.markdown(
        """
        <div class="credit-banner">
            <span>You've used up your daily credits. Upgrade to continue.</span>
            <button class="btn-upgrade-core"><span>+</span> Upgrade to Core</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 6. Replit Search Form: Single-input form with active Enter listener
    with st.form("home_search_form", clear_on_submit=True):
        typed_input = st.text_input(
            "Task",
            placeholder="Start chatting or describe a task...",
            label_visibility="collapsed",
            key="home_search_input",
        )

        st.markdown(
            """
            <div class="console-bottom-toolbar">
                <span style="color:#7E8B9D; font-size:1.15rem; cursor:pointer;">+</span>
                <div style="display:flex; align-items:center; gap:16px; margin-right: 32px;">
                    <div style="display:inline-flex; align-items:center; gap:5px; color:#8E9BAE; font-size:0.82rem; cursor:pointer;">
                        <span>:::</span>
                        <span>Free ▾</span>
                    </div>
                    <span style="color:#7E8B9D; cursor:pointer; font-size:0.95rem;">🎙️</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("↑")

    # Display ongoing chat above the search bar
    if st.session_state.messages:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            role = "assistant" if msg["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(msg["text"])

    # Submission logic: detects Enter key or arrow click
    active_prompt = typed_input if (submitted and typed_input) else clicked_task
    if active_prompt:
        st.session_state.messages.append({"role": "user", "text": active_prompt})

        if is_design_task(active_prompt):
            st.session_state.view_mode = "workspace"
            with st.spinner("⚡ Autonomous Agent composing application..."):
                reply = query_gemini(active_prompt, is_design=True)
                if "```html" in reply:
                    st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                    st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
                else:
                    st.session_state.messages.append({"role": "model", "text": reply})
        else:
            with st.spinner("⚡ Responding..."):
                reply = query_gemini(active_prompt, is_design=False)
                st.session_state.messages.append({"role": "model", "text": reply})

        st.rerun()

# --- WORKSPACE MODE (2-column layout when building) ---
else:
    top_c1, top_c2 = st.columns([7, 3])
    with top_c1:
        st.markdown("### 📁 Ciwi AI Assistant · Live Build")
    with top_c2:
        if st.button("← Back to Home"):
            st.session_state.view_mode = "home"
            st.rerun()

    c_chat, c_prev = st.columns([1, 1], gap="medium")

    with c_chat:
        chat_box = st.container(height=540)
        with chat_box:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["text"])

        if follow := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "text": follow})
            reply = query_gemini(follow, is_design=True)
            if "```html" in reply:
                st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
            else:
                st.session_state.messages.append({"role": "model", "text": reply})
            st.rerun()

    with c_prev:
        components.html(st.session_state.html_code, height=580, scrolling=True)
