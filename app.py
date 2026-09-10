import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Ciwi Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Replit Workspace Precise CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Base */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        overflow-x: hidden;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding: 0.6rem 1rem 0.8rem 1rem !important;
    }

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151C !important;
        border-right: 1px solid #1F242D !important;
        padding-top: 0.8rem !important;
    }

    .sb-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 1rem;
    }

    .sb-brand-icon {
        color: #F26522 !important;
        font-size: 1.35rem;
    }

    .workspace-select {
        background: #181D26;
        border: 1px solid #28303E;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.86rem;
        font-weight: 600;
        color: #CBD5E1;
        margin-bottom: 1.2rem;
    }

    .nav-btn {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.42rem 0.6rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        text-decoration: none;
        margin-bottom: 2px;
        transition: background 0.15s;
    }

    .nav-btn:hover, .nav-btn.active {
        background: #1C222C;
        color: #FFFFFF;
    }

    .recent-header {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        color: #64748B;
        margin: 1.4rem 0 0.4rem 0.4rem;
    }

    .upgrade-card {
        background: #161B23;
        border: 1px solid #262F3E;
        border-radius: 10px;
        padding: 0.8rem 0.9rem;
        margin-top: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Top Workspace Header */
    .top-bar-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .proj-title-pill {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #181D26;
        border: 1px solid #28303E;
        border-radius: 8px;
        padding: 5px 12px;
        font-size: 0.88rem;
        font-weight: 700;
        color: #FFFFFF;
    }

    .mode-tab {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94A3B8;
        cursor: pointer;
        padding: 2px 4px;
    }

    .mode-tab.active {
        color: #F26522;
        border-bottom: 2px solid #F26522;
    }

    /* Action Buttons */
    div.stButton > button {
        background-color: #181D26 !important;
        color: #E2E8F0 !important;
        border: 1px solid #28303E !important;
        border-radius: 8px !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        padding: 0.35rem 0.75rem !important;
    }

    div.stButton > button:hover {
        background-color: #242B38 !important;
        border-color: #3D485C !important;
        color: #FFFFFF !important;
    }

    .publish-box div.stButton > button {
        background-color: #0070F3 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 700 !important;
    }

    .publish-box div.stButton > button:hover {
        background-color: #0060DF !important;
    }

    /* Left Chat & Markdown Output */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 0.4rem 0 !important;
    }

    [data-testid="stChatMessage"] * {
        color: #E2E8F0 !important;
        line-height: 1.6;
    }

    .agent-header-card {
        background: #12161E;
        border: 1px solid #222936;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    .palette-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #251B14;
        border: 1px solid #5C3218;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #F97316;
        margin-bottom: 0.6rem;
    }

    /* Replit Live Project Slide Viewport */
    .viewport-window {
        background: #FFFFFF;
        border: 1px solid #242B38;
        border-radius: 12px;
        overflow: hidden;
        height: 82vh;
        display: flex;
        flex-direction: column;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
    }

    .viewport-browser-bar {
        background: #181D26;
        border-bottom: 1px solid #28303E;
        padding: 0.45rem 0.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .browser-tabs {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #0E1117;
        border: 1px solid #242B38;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.78rem;
        color: #CBD5E1;
        max-width: 160px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .browser-address-bar {
        background: #0E1117;
        border: 1px solid #242B38;
        border-radius: 6px;
        padding: 4px 12px;
        font-size: 0.8rem;
        color: #94A3B8;
        flex-grow: 1;
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: monospace;
    }

    /* Fixed Chat Input Bar */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #151A22 !important;
        border: 1px solid #2A3342 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "project_name" not in st.session_state:
    st.session_state.project_name = "Dine Easy"
if "html_code" not in st.session_state:
    st.session_state.html_code = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #FFF8ED; color: #5C2318; padding: 2rem 1.5rem; }
        .header-logo { text-align: center; margin-bottom: 2rem; }
        .header-logo h2 { color: #28B4C4; font-size: 1.8rem; font-weight: 800; display: inline-flex; align-items: center; gap: 6px; }
        .card { background: #FFFFFF; border-radius: 16px; padding: 2.2rem 1.8rem; max-width: 440px; margin: 0 auto; box-shadow: 0 10px 30px rgba(92, 35, 24, 0.07); border: 1px solid #F1E5D8; }
        .card h1 { color: #28B4C4; font-size: 1.95rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; line-height: 1.2; }
        .card p { color: #7B4B3A; font-size: 0.95rem; text-align: center; margin-bottom: 1.8rem; line-height: 1.5; }
        .field { margin-bottom: 1.2rem; }
        .field label { display: block; font-size: 0.85rem; font-weight: 700; color: #5C2318; margin-bottom: 0.35rem; }
        .field input { width: 100%; padding: 0.8rem 1rem; border: 1.5px solid #E7D8C8; border-radius: 10px; font-size: 0.95rem; outline: none; background: #FAF7F2; }
        .field input:focus { border-color: #28B4C4; background: #FFFFFF; }
        .btn-submit { width: 100%; padding: 0.9rem; background: #28B4C4; color: #FFFFFF; font-size: 1rem; font-weight: 700; border: none; border-radius: 10px; cursor: pointer; transition: 0.15s; margin-top: 0.5rem; }
        .btn-submit:hover { background: #1EA1B0; }
      </style>
    </head>
    <body>
      <div class="header-logo">
        <h2>☕ Bean Board</h2>
      </div>
      <div class="card">
        <h1>Join the Bean Board Family</h1>
        <p>Sign up for exclusive offers, secret menu items, and a special treat on your birthday!</p>
        <div class="field">
          <label>Full Name</label>
          <input type="text" placeholder="John Doe" />
        </div>
        <div class="field">
          <label>WhatsApp Number</label>
          <input type="tel" placeholder="+91 98765 43210" />
        </div>
        <button class="btn-submit" onclick="alert('Welcome to the Bean Board family!')">Join Now</button>
      </div>
    </body>
    </html>
    """

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "model",
            "parts": [
                {
                    "text": (
                        "**Colour palette extracted from the logo:**\n\n"
                        "- **Primary (teal) `#28B4C4`** — used on all buttons, CTAs, category tabs, prices, and the Cart action.\n"
                        "- **Secondary (coffee brown) `#5C2318`** — used as the footer background, heading typography, and secondary actions.\n"
                        "- **Background stays cream `#FFF8ED`** — provides a warm coastal feel.\n\n"
                        "The live project purpose slide is updated and interactive in your right pane."
                    )
                }
            ],
        }
    ]

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sb-brand">
            <span class="sb-brand-icon">⠕</span> Ciwi Agent
        </div>
        <div class="workspace-select">
            <span>📁 Personal workspace</span>
            <span>▾</span>
        </div>
        <a class="nav-btn" href="#">➕ New Repl</a>
        <a class="nav-btn" href="#">📥 Import</a>
        <a class="nav-btn" href="#">📁 Projects</a>
        <a class="nav-btn" href="#">⏱️ Routines <span style="background:#28303E; font-size:0.7rem; padding:1px 6px; border-radius:4px; margin-left:auto; color:#60A5FA;">Beta</span></a>
        <a class="nav-btn" href="#">📚 Library</a>
        <a class="nav-btn" href="#">🔌 Integrations</a>
        <a class="nav-btn" href="#">🔒 Security</a>
        <div class="recent-header">RECENT</div>
        <a class="nav-btn active" href="#">› Dine Easy</a>
        <a class="nav-btn" href="#">› Fashion Showcase</a>
        <div class="upgrade-card">
            <div>
                <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade plan</div>
                <div style="font-size:0.72rem; color:#8B949E;">Unlock GPU credits</div>
            </div>
            <span style="color:#0070F3; font-size:1.2rem;">★</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"Logged in as: **{st.session_state.user_name}**")

# ---------------------------------------------------------
# Top Navigation Header
# ---------------------------------------------------------
h_col_left, h_col_right = st.columns([6, 4])

with h_col_left:
    st.markdown(
        f"""
        <div class="top-bar-left">
            <div class="proj-title-pill">📁 {st.session_state.project_name} ▾</div>
            <span class="mode-tab">Design</span>
            <span class="mode-tab active">Build</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with h_col_right:
    t_c1, t_c2, t_c3 = st.columns([1.2, 1.2, 1.5])
    with t_c1:
        st.button("⚙️ Tools", use_container_width=True)
    with t_c2:
        st.button("👥 Invite", use_container_width=True)
    with t_c3:
        st.markdown('<div class="publish-box">', unsafe_allow_html=True)
        if st.button("🚀 Publish", use_container_width=True):
            st.toast("Published directly to ciwi.replit.dev!", icon="🚀")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main 2-Slide Workspace (Left: Agent Chat | Right: Project Purpose Slide)
# ---------------------------------------------------------
col_left_agent, col_right_project = st.columns([1, 1], gap="large")

# --- Left Slide: Terminal History & Conversation ---
with col_left_agent:
    terminal_box = st.container(height=520)
    with terminal_box:
        st.markdown(
            """
            <div class="agent-header-card">
                <div class="palette-badge">🎨 Theme Architecture</div>
                <h4 style="margin: 0 0 6px 0; color:#FFFFFF;">Active Project Configuration</h4>
                <p style="font-size:0.85rem; color:#94A3B8; margin:0;">Autonomous Agent executing design tokens & live layouts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for m in st.session_state.messages:
            role = "assistant" if m["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(m["parts"][0]["text"])

    # Sticky prompt capsule pinned at base
    if prompt_agent := st.chat_input("Message Agent..."):
        st.session_state.messages.append({"role": "user", "parts": [{"text": prompt_agent}]})
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

        if not api_key:
            st.error("Missing GEMINI_API_KEY in Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            with st.spinner("⚡ Ciwi Agent updating live project slide..."):
                gen_prompt = (
                    f"You are the Ciwi Autonomous Web Engine. The user requested: '{prompt_agent}'.\n"
                    f"Current code base:\n{st.session_state.html_code}\n\n"
                    "Requirements:\n"
                    "1. Provide a bulleted summary of UI/UX updates.\n"
                    "2. Return the complete updated standalone HTML/CSS/JS inside a ```html ``` block."
                )
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=gen_prompt,
                )
                response_text = res.text

                if "```html" in response_text:
                    st.session_state.html_code = response_text.split("```html")[1].split("```")[0].strip()

                st.session_state.messages.append({"role": "model", "parts": [{"text": response_text}]})
                st.rerun()

# --- Right Slide: Live Interactive Project Purpose Slide ---
with col_right_project:
    st.markdown(
        f"""
        <div class="viewport-window">
            <div class="viewport-browser-bar">
                <div class="browser-tabs">
                    <span>Bean Board - Bhe...</span>
                    <span style="font-size: 0.65rem; margin-left:auto;">✕</span>
                </div>
                <div class="browser-address-bar">
                    <span style="color:#64748B;">← → ⟳</span>
                    <span style="color:#38BDF8;">https://</span><span>ciwi.replit.dev/{st.session_state.project_name.lower().replace(' ', '-')}</span>
                </div>
                <div style="color:#94A3B8; font-size:0.85rem;">◰</div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Clean embedded execution iframe
    components.html(st.session_state.html_code, height=520, scrolling=True)

    st.markdown("</div>", unsafe_allow_html=True)
