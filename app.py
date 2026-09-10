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
    /* Dark canvas with authentic bottom amber glow */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #101216 !important;
        background-image: radial-gradient(ellipse 75% 45% at 50% 90%, rgba(135, 45, 15, 0.38) 0%, rgba(16, 18, 22, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 860px !important;
        padding-top: 5rem !important;
        padding-bottom: 4rem !important;
        margin: 0 auto !important;
    }

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1D2330 !important;
    }

    /* Main Greeting */
    .replit-hero-title {
        font-size: 2.45rem;
        font-weight: 600;
        letter-spacing: -0.025em;
        color: #F3F4F6;
        margin-bottom: 1.4rem;
    }

    /* Suggested for you label */
    .suggested-label {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.8rem;
        color: #8C96A5;
        margin-bottom: 0.75rem;
    }

    /* Stacked Pill Buttons */
    .pill-stack {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        align-items: flex-start;
        margin-bottom: 1.25rem;
    }

    .replit-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: #1A1E27;
        border: 1px solid #2B3240;
        border-radius: 9999px;
        padding: 6px 14px;
        font-size: 0.86rem;
        color: #D1D5DB;
        cursor: pointer;
        transition: all 0.15s ease;
        text-decoration: none;
    }

    .replit-pill:hover {
        background-color: #232936;
        border-color: #3B4557;
        color: #FFFFFF;
    }

    /* 2-Row Console Card Form */
    [data-testid="stForm"] {
        background-color: #1A1E27 !important;
        border: 1px solid #2B3342 !important;
        border-radius: 14px !important;
        padding: 0.85rem 1rem 0.65rem 1.1rem !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #4A5568 !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6) !important;
    }

    /* Remove Streamlit default input containers */
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

    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 0.98rem !important;
        color: #F3F4F6 !important;
        padding: 0.2rem 0 1.2rem 0 !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #647082 !important;
    }

    /* Console Bottom Row Elements */
    .console-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-top: 0.35rem;
    }

    .console-left-icon {
        color: #7E8B9D;
        display: flex;
        align-items: center;
        font-size: 1.15rem;
        cursor: pointer;
    }

    .console-right-group {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .model-selector {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: #9CA3AF;
        font-size: 0.8rem;
        cursor: pointer;
    }

    .model-selector svg {
        fill: currentColor;
    }

    .mic-icon {
        color: #7E8B9D;
        display: flex;
        align-items: center;
        cursor: pointer;
    }

    /* Submit Button (Styled as Arrow Icon) */
    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: transparent !important;
        border: none !important;
        color: #7E8B9D !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0 !important;
        margin: 0 !important;
        min-width: 22px !important;
        width: 22px !important;
        height: 22px !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: color 0.15s ease;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        color: #F3F4F6 !important;
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

# Sidebar matching previous structure
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 0.2rem 0.4rem 1rem 0.4rem;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522"><path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/></svg>
            <div style="display:flex; gap:12px; color:#8B949E;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Logged in as **{st.session_state.user_name}**")

# --- Exact Home Interface ---
if st.session_state.view_mode == "home":
    # 1. Headline
    st.markdown(
        f'<div class="replit-hero-title">{st.session_state.user_name}, what are we working on today?</div>',
        unsafe_allow_html=True,
    )

    # 2. Suggested Label + Refresh Icon
    st.markdown(
        """
        <div class="suggested-label">
            <span>Suggested for you</span>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" style="cursor:pointer;"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.19"/></svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3. Vertically Stacked Pill Buttons
    p1, p_rest = st.columns([4, 6])
    with p1:
        clicked_task = None
        if st.button("✦  Help me get things done", key="pill_1", use_container_width=True):
            clicked_task = "Build a productivity tasks dashboard with drag-and-drop workflow"
        if st.button("⮦  Review Resend delivery", key="pill_2", use_container_width=True):
            clicked_task = "Build an email log and resend webhook monitor"

    # 4. Input Console Box
    with st.form("replit_console_form", clear_on_submit=False):
        prompt_val = st.text_input(
            "Task",
            placeholder="Start chatting or describe a task...",
            label_visibility="collapsed",
        )

        b_left, b_mid, b_right = st.columns([1, 8, 1])
        with b_left:
            st.markdown(
                """
                <div class="console-left-icon">
                    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14m-7-7h14"/></svg>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with b_mid:
            st.markdown(
                """
                <div style="display:flex; justify-content:flex-end; align-items:center; gap:16px; height:100%;">
                    <div class="model-selector">
                        <svg width="12" height="12" viewBox="0 0 24 24"><circle cx="4" cy="4" r="2"/><circle cx="12" cy="4" r="2"/><circle cx="20" cy="4" r="2"/><circle cx="4" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="20" cy="12" r="2"/><circle cx="4" cy="20" r="2"/><circle cx="12" cy="20" r="2"/><circle cx="20" cy="20" r="2"/></svg>
                        <span>Free</span>
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                    </div>
                    <div class="mic-icon">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with b_right:
            submitted = st.form_submit_button("↑")

    # Handle Submission and Transition to Split Screen
    active_prompt = prompt_val if (submitted and prompt_val) else clicked_task
    if active_prompt:
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            st.error("Missing GEMINI_API_KEY in Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            st.session_state.view_mode = "workspace"
            st.session_state.messages.append({"role": "user", "parts": [{"text": active_prompt}]})

            with st.spinner("⚡ Autonomous Agent composing application..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Build an interactive web application for: '{active_prompt}'.\n"
                        "1. Provide a bulleted summary of UI components and colors.\n"
                        "2. Provide complete standalone HTML/CSS/JS inside a ```html ``` block."
                    ),
                )
                output = res.text
                if "```html" in output:
                    st.session_state.html_code = output.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

# --- Dual Pane Live Workspace (When building) ---
else:
    col_chat, col_preview = st.columns([1, 1], gap="medium")

    with col_chat:
        container = st.container(height=520)
        with container:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["parts"][0]["text"])

        if follow_up := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "parts": [{"text": follow_up}]})
            api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            client = genai.Client(api_key=api_key)
            with st.spinner("⚡ Updating application..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Current code:\n{st.session_state.html_code}\n\n"
                        f"User request: {follow_up}\n"
                        "Return brief explanation + updated code in ```html ``` block."
                    ),
                )
                if "```html" in res.text:
                    st.session_state.html_code = res.text.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": res.text}]})
                st.rerun()

    with col_preview:
        components.html(st.session_state.html_code, height=560, scrolling=True)
