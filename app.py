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
    /* Dark background and glow */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        background-image: radial-gradient(ellipse 70% 40% at 50% 88%, rgba(160, 55, 20, 0.28) 0%, rgba(14, 17, 23, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 820px !important;
        padding-top: 4.5rem !important;
        padding-bottom: 4rem !important;
        margin: 0 auto !important;
    }

    /* Sidebar container */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1C222E !important;
    }

    .sb-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.2rem 0.8rem 0.2rem;
    }

    .sb-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        font-weight: 500;
        cursor: pointer;
        transition: 0.15s ease;
    }

    .sb-item:hover {
        background-color: #181E29;
        color: #FFFFFF;
    }

    .sb-item-active {
        background-color: #181E29;
        color: #FFFFFF;
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

    .beta-tag {
        background: #19273D;
        color: #38BDF8;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
        margin-left: auto;
    }

    .sb-heading {
        font-size: 0.74rem;
        font-weight: 700;
        color: #64748B;
        padding: 1rem 0.4rem 0.3rem 0.4rem;
    }

    .upgrade-box {
        background: #151A24;
        border: 1px solid #232B39;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Fixed Pill Buttons (Overriding default white backgrounds) */
    div.stButton > button {
        background-color: #1A1E27 !important;
        color: #E2E8F0 !important;
        border: 1px solid #2C3545 !important;
        border-radius: 9999px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 1.1rem !important;
        display: inline-flex !important;
        align-items: center !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.15s ease-in-out !important;
        width: auto !important;
        margin-bottom: 0.45rem !important;
    }

    div.stButton > button:hover {
        background-color: #232936 !important;
        border-color: #475569 !important;
        color: #FFFFFF !important;
    }

    /* Console form */
    [data-testid="stForm"] {
        background-color: #161A23 !important;
        border: 1px solid #252D3C !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.1rem 0.6rem 1.1rem !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5) !important;
        margin-top: 0.8rem !important;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #384357 !important;
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

    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 0.98rem !important;
        color: #F8FAFC !important;
        padding: 0.2rem 0 1.2rem 0 !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #556275 !important;
    }

    .console-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #1C2330;
        padding-top: 0.5rem;
    }

    .tool-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: #8E9BAE;
        font-size: 0.82rem;
        cursor: pointer;
    }

    /* Arrow button */
    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: transparent !important;
        border: none !important;
        color: #8E9BAE !important;
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
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state initialization
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "html_code" not in st.session_state:
    st.session_state.html_code = ""

# --- Sidebar UI ---
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
                <span style="font-size:1rem;">👤</span>
                <span>Personal workspace</span>
            </div>
            <span>▾</span>
        </div>

        <div class="new-btn">
            <span style="font-weight:700;">+</span>
            <span>New</span>
        </div>

        <div class="sb-item"><span>📥</span> <span>Import</span></div>
        <div class="sb-item"><span>📁</span> <span>Projects</span></div>
        <div class="sb-item"><span>⏱️</span> <span>Routines</span> <span class="beta-tag">Beta</span></div>
        <div class="sb-item"><span>📚</span> <span>Library</span></div>
        <div class="sb-item"><span>🔌</span> <span>Integrations</span></div>
        <div class="sb-item"><span>🛡️</span> <span>Security</span></div>

        <div class="sb-heading">Recent</div>
        <div class="sb-item"><span>🗂️</span> <span>Fashion Showcase</span></div>
        <div class="sb-item sb-item-active"><span>🗂️</span> <span>Dine Easy</span></div>

        <div class="upgrade-box">
            <div>
                <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
                <div style="font-size:0.72rem; color:#8B949E; margin-top:2px;">Unlock more credits</div>
            </div>
            <div style="background:#0070F3; border-radius:6px; width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#FFF; font-weight:700;">✦</div>
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

# --- Main View ---
if st.session_state.view_mode == "home":
    st.markdown(
        f'<div style="font-size:2.45rem; font-weight:600; color:#F3F4F6; margin-bottom:1.4rem;">{st.session_state.user_name}, what are we working on today?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:6px; font-size:0.82rem; color:#8C96A5; margin-bottom:0.75rem;">
            <span>Suggested for you</span>
            <span style="cursor:pointer;">⟳</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    clicked_task = None
    if st.button("✨  Help me get things done", key="btn_help"):
        clicked_task = "Build a productivity tasks dashboard with drag-and-drop workflow"
    if st.button("↪  Review Resend delivery", key="btn_resend"):
        clicked_task = "Build an email log and resend webhook monitor"

    with st.form("main_chat_form", clear_on_submit=False):
        prompt_val = st.text_input(
            "Task",
            placeholder="Start chatting or describe a task...",
            label_visibility="collapsed",
        )

        st.markdown(
            """
            <div class="console-footer">
                <span style="color:#7E8B9D; font-size:1.1rem; cursor:pointer;">+</span>
                <div style="display:flex; align-items:center; gap:14px;">
                    <div class="tool-pill">
                        <span>:::</span>
                        <span>Free ▾</span>
                    </div>
                    <span style="color:#7E8B9D; cursor:pointer;">🎙️</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sub_col1, sub_col2 = st.columns([15, 1])
        with sub_col2:
            submitted = st.form_submit_button("↑")

    active_prompt = prompt_val if (submitted and prompt_val) else clicked_task
    if active_prompt:
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            st.error("Missing GEMINI_API_KEY in Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            st.session_state.view_mode = "workspace"
            st.session_state.messages.append({"role": "user", "parts": [{"text": active_prompt}]})

            with st.spinner("⚡ Ciwi Agent generating workspace..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Build an interactive web application for: '{active_prompt}'.\n"
                        "1. Summary of design tokens.\n"
                        "2. Return complete code inside a ```html ``` block."
                    ),
                )
                output = res.text
                if "```html" in output:
                    st.session_state.html_code = output.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

else:
    # 2-Column Live Workspace
    top_col1, top_col2 = st.columns([6, 4])
    with top_col1:
        st.markdown("### 📁 Active Build · Dine Easy")
    with top_col2:
        if st.button("← Back to Home"):
            st.session_state.view_mode = "home"
            st.rerun()

    c_chat, c_prev = st.columns([1, 1], gap="medium")
    with c_chat:
        chat_box = st.container(height=520)
        with chat_box:
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
                        f"Request: {follow_up}\n"
                        "Return code in ```html ``` block."
                    ),
                )
                if "```html" in res.text:
                    st.session_state.html_code = res.text.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": res.text}]})
                st.rerun()

    with c_prev:
        components.html(st.session_state.html_code, height=560, scrolling=True)
