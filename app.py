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
    /* Full-screen Dark Canvas */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    /* Expand full screen across both panes */
    .main .block-container {
        max-width: 100% !important;
        padding: 1rem 1.5rem 2rem 1.5rem !important;
    }

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1C222E !important;
    }

    .sb-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 7px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        font-weight: 500;
        cursor: pointer;
    }

    .sb-item:hover, .sb-item-active {
        background-color: #181E29;
        color: #FFFFFF !important;
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

    /* Button Styling */
    div.stButton > button {
        background-color: #1A1E27 !important;
        color: #E2E8F0 !important;
        border: 1px solid #2C3545 !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        padding: 0.4rem 0.9rem !important;
    }

    div.stButton > button:hover {
        background-color: #232936 !important;
        border-color: #475569 !important;
        color: #FFFFFF !important;
    }

    /* High-contrast Chat Area */
    [data-testid="stChatMessage"] {
        background-color: #161A23 !important;
        border: 1px solid #242B38 !important;
        border-radius: 10px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stChatMessage"] * {
        color: #F3F4F6 !important;
        line-height: 1.5 !important;
    }

    /* Chat Input Bar */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #161A23 !important;
        border: 1px solid #252D3C !important;
        border-radius: 12px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    /* Right Preview Browser Window */
    .preview-window {
        background-color: #FFFFFF;
        border: 1px solid #232B39;
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        height: calc(85vh - 40px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .preview-header {
        background-color: #161A23;
        border-bottom: 1px solid #232B39;
        padding: 0.5rem 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .preview-url {
        background-color: #0E1117;
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

# Session initialization
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "project_name" not in st.session_state:
    st.session_state.project_name = "Dine Easy"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "workspace"
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "text": "Welcome back! What features would you like to add to Dine Easy?"}
    ]
if "html_code" not in st.session_state or not st.session_state.html_code:
    st.session_state.html_code = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #FFF8ED; color: #5C2318; padding: 2.5rem 1.5rem; text-align: center; }
        .card { background: #FFFFFF; border-radius: 16px; padding: 2rem 1.5rem; max-width: 400px; margin: 0 auto; box-shadow: 0 10px 25px rgba(92,35,24,0.08); }
        h1 { color: #28B4C4; font-size: 1.8rem; margin-bottom: 0.5rem; }
        p { color: #7B4B3A; font-size: 0.95rem; margin-bottom: 1.5rem; }
        input { width: 100%; padding: 0.75rem 1rem; border: 1.5px solid #E7D8C8; border-radius: 8px; margin-bottom: 1rem; outline: none; font-size: 0.95rem; }
        button { width: 100%; padding: 0.85rem; background: #28B4C4; color: #FFFFFF; font-weight: 700; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Dine Easy</h1>
        <p>Book a table or order online in seconds.</p>
        <input type="text" placeholder="Your Name" />
        <input type="tel" placeholder="Phone Number" />
        <button onclick="alert('Reservation confirmed!')">Reserve Table</button>
      </div>
    </body>
    </html>
    """

def query_agent(prompt: str):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Missing GEMINI_API_KEY in Secrets."
    client = genai.Client(api_key=api_key)

    system_instruction = (
        "You are Ciwi, an elite autonomous web agent identical to Replit Agent.\n"
        "Guidelines:\n"
        "1. If the user says a conversational greeting or general statement (e.g. 'hi', 'hello', 'who are you'), "
        "reply helpfully in 1-2 friendly sentences. Do NOT generate HTML code for greetings.\n"
        "2. If the user asks to build, modify, redesign, or add a feature, explain the changes concisely in markdown "
        "bullet points, and output the complete standalone HTML/CSS/JS strictly inside a ```html ``` block."
    )
    context = f"Current App Code:\n{st.session_state.html_code}\n\nUser request: {prompt}"
    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=context,
        config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.7),
    )
    return res.text

# --- Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; padding: 0.2rem 0.2rem 0.8rem 0.2rem;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522"><path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/></svg>
            <div style="display:flex; gap:12px; color:#8B949E;"><span>🔍</span><span>◫</span></div>
        </div>
        <div class="workspace-pill">
            <div style="display:flex; align-items:center; gap:8px;"><span>👤</span><span>Personal workspace</span></div>
            <span>▾</span>
        </div>
        <div class="new-btn"><span>+</span><span>New</span></div>
        <div class="sb-item"><span>📥</span> <span>Import</span></div>
        <div class="sb-item"><span>📁</span> <span>Projects</span></div>
        <div class="sb-item"><span>⏱️</span> <span>Routines</span></div>
        <div class="sb-item"><span>📚</span> <span>Library</span></div>
        <div class="sb-item"><span>🔌</span> <span>Integrations</span></div>
        <div class="sb-item"><span>🛡️</span> <span>Security</span></div>
        <div style="font-size:0.74rem; font-weight:700; color:#64748B; padding:1rem 0.4rem 0.3rem 0.4rem;">Recent</div>
        <div class="sb-item"><span>🗂️</span> <span>Fashion Showcase</span></div>
        <div class="sb-item sb-item-active"><span>🗂️</span> <span>Dine Easy</span></div>
        <div class="upgrade-box">
            <div>
                <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade plan</div>
                <div style="font-size:0.72rem; color:#8B949E;">Unlock GPU credits</div>
            </div>
            <span style="color:#0070F3; font-size:1.1rem; font-weight:bold;">✦</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Top Navigation Bar ---
top_l, top_r = st.columns([7, 3])
with top_l:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; padding-top: 4px;">
            <span style="background:#181E28; border:1px solid #232B39; padding:4px 12px; border-radius:6px; font-weight:700; font-size:0.88rem; color:#FFFFFF;">📁 {st.session_state.project_name} ▾</span>
            <span style="color:#94A3B8; font-size:0.84rem; font-weight:600;">Design</span>
            <span style="color:#F26522; font-size:0.84rem; font-weight:700; border-bottom:2px solid #F26522; padding-bottom:1px;">Build</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_r:
    col_tools, col_invite, col_pub = st.columns(3)
    with col_tools:
        st.button("⚙️ Tools", use_container_width=True)
    with col_invite:
        st.button("👥 Invite", use_container_width=True)
    with col_pub:
        if st.button("🚀 Publish", use_container_width=True):
            st.toast("Published to ciwi.replit.dev!", icon="🚀")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# --- Full-Width Dual Column Workspace ---
col_chat, col_preview = st.columns([1, 1], gap="large")

with col_chat:
    chat_box = st.container(height=560)
    with chat_box:
        for m in st.session_state.messages:
            role = "assistant" if m["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(m["text"])

    if user_msg := st.chat_input("Message Agent..."):
        st.session_state.messages.append({"role": "user", "text": user_msg})
        with st.spinner("⚡ Ciwi Agent responding..."):
            reply = query_agent(user_msg)
            if "```html" in reply:
                parts = reply.split("```html")
                chat_summary = parts[0].strip()
                code_body = parts[1].split("```")[0].strip()
                st.session_state.html_code = code_body
                st.session_state.messages.append({
                    "role": "model",
                    "text": chat_summary if chat_summary else "Application updated and deployed to live preview."
                })
            else:
                st.session_state.messages.append({"role": "model", "text": reply})
        st.rerun()

with col_preview:
    st.markdown(
        f"""
        <div class="preview-header" style="border-radius: 12px 12px 0 0;">
            <span style="background:#0E1117; border:1px solid #232B39; border-radius:6px; padding:3px 10px; font-size:0.78rem; color:#CBD5E1;">{st.session_state.project_name} ✕</span>
            <div class="preview-url">[https://ciwi.replit.dev/](https://ciwi.replit.dev/){st.session_state.project_name.lower().replace(' ', '-')}</div>
            <span style="color:#8B949E; font-size:0.85rem; cursor:pointer;">⟳</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    components.html(st.session_state.html_code, height=520, scrolling=True)
