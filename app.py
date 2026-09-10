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

    /* Workspace mode full width */
    .workspace-mode .main .block-container {
        max-width: 100% !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
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

    /* Pill buttons */
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

    /* Form console */
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

    /* Live Sandbox Shell */
    .sandbox-shell {
        background-color: #12151D;
        border: 1px solid #232B39;
        border-radius: 14px;
        overflow: hidden;
        height: 80vh;
        display: flex;
        flex-direction: column;
    }

    .sandbox-header {
        background-color: #181E29;
        border-bottom: 1px solid #232B39;
        padding: 0.5rem 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .sandbox-url {
        background: #0E1117;
        border: 1px solid #232B39;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.78rem;
        color: #94A3B8;
        flex-grow: 1;
        font-family: monospace;
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
    st.session_state.html_code = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { font-family: -apple-system, sans-serif; background: #FFF8ED; color: #5C2318; padding: 2rem; text-align: center; }
        .card { background: white; border-radius: 12px; padding: 2rem; max-width: 380px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
        h1 { color: #28B4C4; margin-bottom: 0.5rem; }
        button { background: #28B4C4; color: white; border: none; padding: 0.8rem 1.4rem; border-radius: 8px; font-weight: bold; cursor: pointer; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Dine Easy</h1>
        <p>Your interactive restaurant workspace preview.</p>
        <button onclick="alert('Ready to build!')">Get Started</button>
      </div>
    </body>
    </html>
    """

# Agent helper function
def query_agent(prompt: str):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Missing GEMINI_API_KEY in Secrets."

    client = genai.Client(api_key=api_key)

    system_prompt = (
        "You are Ciwi, an elite autonomous web development AI identical to Replit Agent. "
        "User context: The current user is Mahesh. "
        "Guidelines:\n"
        "1. If the user says a conversational greeting (e.g. 'hi', 'hello', 'hey', 'who are you', 'how are you'), "
        "reply warmly and concisely as an AI agent ready to build software. Do NOT write HTML or code for greetings.\n"
        "2. If the user asks to create, modify, build, or fix a web app/feature, explain your changes in 2-3 clean bullet points, "
        "and provide the complete standalone code strictly within a ```html ``` block."
    )

    full_context = f"Current App Code:\n{st.session_state.html_code}\n\nUser request: {prompt}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=full_context,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7,
        ),
    )
    return response.text

# --- Left Sidebar ---
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

# --- Home View ---
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
        st.session_state.view_mode = "workspace"
        st.session_state.messages.append({"role": "user", "text": active_prompt})

        with st.spinner("⚡ Ciwi Agent thinking..."):
            reply = query_agent(active_prompt)

            # Separate code from chat text
            if "```html" in reply:
                parts = reply.split("```html")
                chat_text = parts[0].strip()
                code_text = parts[1].split("```")[0].strip()
                st.session_state.html_code = code_text
                st.session_state.messages.append({
                    "role": "model",
                    "text": chat_text if chat_text else "I've generated and deployed the application to your right preview panel."
                })
            else:
                st.session_state.messages.append({"role": "model", "text": reply})

        st.rerun()

# --- 2-Column Split Workspace ---
else:
    top_col1, top_col2 = st.columns([7, 3])
    with top_col1:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; margin-bottom: 0.6rem;">
                <span style="background:#181E28; border:1px solid #232B39; padding:4px 10px; border-radius:6px; font-weight:700; font-size:0.85rem; color:#FFF;">📁 Dine Easy ▾</span>
                <span style="color:#94A3B8; font-size:0.82rem; font-weight:600;">Design</span>
                <span style="color:#F26522; font-size:0.82rem; font-weight:700; border-bottom:2px solid #F26522;">Build</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_col2:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.view_mode = "home"
            st.rerun()

    c_chat, c_prev = st.columns([1, 1], gap="medium")

    # Left: Agent Chat
    with c_chat:
        chat_box = st.container(height=520)
        with chat_box:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["text"])

        if follow_up := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "text": follow_up})
            with st.spinner("⚡ Ciwi Agent responding..."):
                reply = query_agent(follow_up)

                if "```html" in reply:
                    parts = reply.split("```html")
                    chat_text = parts[0].strip()
                    code_text = parts[1].split("```")[0].strip()
                    st.session_state.html_code = code_text
                    st.session_state.messages.append({
                        "role": "model",
                        "text": chat_text if chat_text else "Updated application deployed to live preview."
                    })
                else:
                    st.session_state.messages.append({"role": "model", "text": reply})

            st.rerun()

    # Right: Browser Viewport
    with c_prev:
        st.markdown(
            """
            <div class="sandbox-shell">
                <div class="sandbox-header">
                    <span style="background:#0E1117; border:1px solid #232B39; border-radius:6px; padding:2px 8px; font-size:0.75rem; color:#CBD5E1;">Dine Easy ✕</span>
                    <div class="sandbox-url">https://ciwi.replit.dev/dine-easy</div>
                    <span style="color:#8B949E; font-size:0.8rem; cursor:pointer;">⟳</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        components.html(st.session_state.html_code, height=520, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)
