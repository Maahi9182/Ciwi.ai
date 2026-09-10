import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Ciwi AI - Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Polished Replit Dark Contrast CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Dark canvas & high-contrast typography */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #F0F6FC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding: 0.6rem 1.4rem 2rem 1.4rem !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid #30363D !important;
    }

    [data-testid="stSidebar"] * {
        color: #C9D1D9 !important;
    }

    .sb-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.3rem;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 1.2rem;
    }

    .sb-brand-icon {
        color: #F26522 !important;
        font-size: 1.4rem;
    }

    .workspace-badge {
        background: #21262D;
        border: 1px solid #30363D;
        padding: 0.5rem 0.8rem;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #F0F6FC !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.2rem;
    }

    .nav-link {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.45rem 0.6rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #8B949E !important;
        text-decoration: none;
        margin-bottom: 2px;
        transition: 0.15s ease;
    }

    .nav-link:hover, .nav-link.active {
        background: #21262D;
        color: #FFFFFF !important;
    }

    .upgrade-box {
        background: #1C2128;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 0.9rem;
        margin-top: 1.8rem;
        margin-bottom: 1rem;
    }

    /* Streamlit Default Buttons to Replit Dark Pill Style */
    div.stButton > button {
        background-color: #21262D !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        font-size: 0.86rem !important;
        font-weight: 600 !important;
        padding: 0.35rem 0.8rem !important;
        transition: all 0.15s ease-in-out !important;
    }

    div.stButton > button:hover {
        background-color: #30363D !important;
        border-color: #8B949E !important;
        color: #FFFFFF !important;
    }

    /* Blue Publish Button */
    .publish-btn div.stButton > button {
        background-color: #0070F3 !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 2px 10px rgba(0, 112, 243, 0.3) !important;
    }

    .publish-btn div.stButton > button:hover {
        background-color: #0060DF !important;
    }

    /* Middle Terminal & Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    [data-testid="stChatMessage"] * {
        color: #F0F6FC !important;
    }

    /* Bottom Chat Input */
    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    div[data-testid="stChatInput"] {
        background-color: #161B22 !important;
        border: 1px solid #30363D !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
    }

    /* Browser Mockup Container */
    .browser-box {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }

    .browser-header {
        background-color: #21262D;
        border-bottom: 1px solid #30363D;
        padding: 0.5rem 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }

    .mac-dots {
        display: flex;
        gap: 6px;
    }

    .mac-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }

    .browser-address {
        background-color: #0E1117;
        border: 1px solid #30363D;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.8rem;
        color: #8B949E;
        flex-grow: 1;
        font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State Initialization
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
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #FFF8ED; color: #5C2318; margin: 0; padding: 2rem; text-align: center; }
        h1 { color: #28B4C4; font-size: 2.2rem; margin-bottom: 0.4rem; font-weight: 800; }
        p { color: #7B4B3A; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.5; }
        .card { background: #FFFFFF; border-radius: 14px; padding: 2rem; max-width: 380px; margin: 0 auto; box-shadow: 0 10px 30px rgba(92,35,24,0.06); }
        input { width: 100%; box-sizing: border-box; padding: 0.75rem 0.9rem; margin-bottom: 0.9rem; border: 1.5px solid #EADBCE; border-radius: 8px; outline: none; font-size: 0.92rem; }
        input:focus { border-color: #28B4C4; }
        button { width: 100%; padding: 0.8rem; background: #28B4C4; color: #FFFFFF; font-weight: 700; border: none; border-radius: 8px; font-size: 0.95rem; cursor: pointer; }
        button:hover { background: #2096A5; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Bean Board Family</h1>
        <p>Sign up for exclusive offers, secret menu items, and a special treat on your birthday!</p>
        <input type="text" placeholder="Full Name" />
        <input type="tel" placeholder="WhatsApp Number" />
        <button onclick="alert('Submitted successfully!')">Join Now</button>
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
                        "### 🎨 Palette Extracted from Logo\n\n"
                        "* **Primary (teal) `#28B4C4`**: Buttons, CTAs, tab states\n"
                        "* **Secondary (coffee brown) `#5C2318`**: Header text and card borders\n"
                        "* **Background cream `#FFF8ED`**: Warm storefront base\n\n"
                        "Live interactive site loaded in the right pane. Provide adjustments or click **Publish**."
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
        <div class="workspace-badge">
            <span>Personal workspace</span>
            <span>▾</span>
        </div>
        <a class="nav-link" href="#">➕ New Repl</a>
        <a class="nav-link" href="#">📥 Import</a>
        <a class="nav-link" href="#">📁 Projects</a>
        <a class="nav-link" href="#">⏱️ Routines <span style="background:#283347; font-size:0.7rem; padding:1px 5px; border-radius:4px; margin-left:auto; color:#60A5FA;">Beta</span></a>
        <a class="nav-link" href="#">📚 Library</a>
        <a class="nav-link" href="#">🔌 Integrations</a>
        <a class="nav-link" href="#">🔒 Security</a>
        <div style="font-size:0.75rem; color:#6E7681; margin: 1.2rem 0 0.4rem 0.5rem; font-weight:700;">RECENT</div>
        <a class="nav-link active" href="#">› Dine Easy</a>
        <a class="nav-link" href="#">› Fashion Showcase</a>
        <div class="upgrade-box">
            <div style="font-size:0.85rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
            <div style="font-size:0.75rem; color:#8B949E; margin-top:3px;">Unlock unlimited GPU & model credits</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"👤 **{st.session_state.user_name}**")

# ---------------------------------------------------------
# Top Bar Navigation
# ---------------------------------------------------------
top_l, top_r = st.columns([6, 4])

with top_l:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:12px; padding-top: 4px;">
            <div style="background:#21262D; border:1px solid #30363D; border-radius:8px; padding:4px 10px; font-weight:700; font-size:0.88rem; color:#FFFFFF;">
                📁 {st.session_state.project_name} ▾
            </div>
            <span style="color:#8B949E; font-size:0.85rem; font-weight:600; cursor:pointer;">Design</span>
            <span style="color:#F26522; font-size:0.85rem; font-weight:700; border-bottom: 2px solid #F26522; padding-bottom: 2px;">Build</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_r:
    b1, b2, b3 = st.columns([1, 1, 1.2])
    with b1:
        st.button("⚙️ Tools", use_container_width=True)
    with b2:
        st.button("👥 Invite", use_container_width=True)
    with b3:
        st.markdown('<div class="publish-btn">', unsafe_allow_html=True)
        if st.button("🚀 Publish", use_container_width=True):
            st.toast("Application published to https://ciwi.replit.dev!", icon="🚀")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main 2-Column Split: Terminal (Left) | Live Sandbox (Right)
# ---------------------------------------------------------
col_agent, col_preview = st.columns([1, 1], gap="medium")

# --- Left Column: Chat History & Agent Conversation ---
with col_agent:
    chat_box = st.container(height=520)
    with chat_box:
        for m in st.session_state.messages:
            role = "assistant" if m["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(m["parts"][0]["text"])

    # Pinned Prompt Input
    if prompt_text := st.chat_input("Message Agent..."):
        st.session_state.messages.append({"role": "user", "parts": [{"text": prompt_text}]})
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

        if not api_key:
            st.error("Please add GEMINI_API_KEY in Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            with st.spinner("⚡ Ciwi Agent is modifying app..."):
                gen_prompt = (
                    f"You are the Ciwi Web Agent. The user wants: '{prompt_text}'.\n"
                    f"Current code:\n{st.session_state.html_code}\n\n"
                    "Requirements:\n"
                    "1. Explain modifications succinctly in bullet points.\n"
                    "2. Return the complete updated code inside a ```html ``` block."
                )
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=gen_prompt,
                )
                output = res.text

                if "```html" in output:
                    parsed = output.split("```html")[1].split("```")[0].strip()
                    st.session_state.html_code = parsed

                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

# --- Right Column: Clean Replit Browser Container ---
with col_preview:
    st.markdown(
        f"""
        <div class="browser-box">
            <div class="browser-header">
                <div class="mac-dots">
                    <div class="mac-dot" style="background:#FF5F56;"></div>
                    <div class="mac-dot" style="background:#FFBD2E;"></div>
                    <div class="mac-dot" style="background:#27C93F;"></div>
                </div>
                <div class="browser-address">[https://ciwi.replit.dev/](https://ciwi.replit.dev/){st.session_state.project_name.lower().replace(' ', '-')}</div>
                <span style="color:#8B949E; font-size:0.8rem; cursor:pointer;">⟳</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Live Executed HTML App
    components.html(st.session_state.html_code, height=520, scrolling=True)
