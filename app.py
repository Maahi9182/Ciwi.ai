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
# Full Replit Dark Workspace CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Dark Obsidian Base Theme */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0E1117 !important;
        color: #E6EDF3 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding: 0.8rem 1.2rem 1.2rem 1.2rem !important;
    }

    /* Left Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #12171F !important;
        border-right: 1px solid #1E2633 !important;
    }

    .sb-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.25rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 1.2rem;
    }

    .sb-brand-icon {
        color: #F26522;
        font-size: 1.4rem;
    }

    .workspace-badge {
        background: #1B2230;
        border: 1px solid #283347;
        padding: 0.45rem 0.8rem;
        border-radius: 8px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #CBD5E1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.45rem 0.6rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        text-decoration: none;
        margin-bottom: 2px;
    }

    .nav-item:hover {
        background: #1B2230;
        color: #FFFFFF;
    }

    .upgrade-box {
        background: #161D29;
        border: 1px solid #232E42;
        border-radius: 10px;
        padding: 0.8rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Top Workspace Header */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #1E2633;
        margin-bottom: 0.8rem;
    }

    .project-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #1A212D;
        border: 1px solid #283347;
        border-radius: 8px;
        padding: 4px 12px;
        font-size: 0.88rem;
        font-weight: 600;
        color: #F1F5F9;
    }

    /* Browser Mockup Window (Right Panel) */
    .browser-frame {
        background: #161B22;
        border: 1px solid #283347;
        border-radius: 12px;
        overflow: hidden;
        height: 82vh;
        display: flex;
        flex-direction: column;
    }

    .browser-toolbar {
        background: #1A212D;
        padding: 0.45rem 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        border-bottom: 1px solid #283347;
    }

    .browser-dots {
        display: flex;
        gap: 6px;
    }

    .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #374151;
    }

    .browser-url-bar {
        background: #0D1117;
        border: 1px solid #283347;
        border-radius: 6px;
        padding: 2px 10px;
        font-size: 0.78rem;
        color: #94A3B8;
        flex-grow: 1;
    }

    /* Bottom-Pinned Agent Input Capsule */
    div[data-testid="stChatInput"] {
        background: #161B22 !important;
        border: 1px solid #2D3748 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    div[data-testid="stChatInput"] textarea {
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
    }

    /* Streamlit Chat Message Adjustments */
    [data-testid="stChatMessage"] {
        background: #131720 !important;
        border: 1px solid #1E2633 !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.8rem !important;
    }

    /* Blue Publish Button */
    .publish-btn div.stButton > button {
        background-color: #0070F3 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.35rem 0.8rem !important;
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
    # Starter interactive template
    st.session_state.html_code = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #FFF8ED; color: #5C2318; margin: 0; padding: 2.5rem; text-align: center; }
        h1 { color: #28B4C4; font-size: 2.2rem; margin-bottom: 0.4rem; }
        p { color: #7B4B3A; font-size: 1rem; margin-bottom: 1.5rem; }
        .card { background: #FFFFFF; border-radius: 16px; padding: 2rem; max-width: 440px; margin: 0 auto; box-shadow: 0 8px 30px rgba(92,35,24,0.08); }
        input { width: 100%; box-sizing: border-box; padding: 0.75rem 1rem; margin-bottom: 1rem; border: 1.5px solid #EADBCE; border-radius: 8px; outline: none; font-size: 0.95rem; }
        input:focus { border-color: #28B4C4; }
        button { width: 100%; padding: 0.85rem; background: #28B4C4; color: #FFFFFF; font-weight: 700; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #2096A5; }
      </style>
    </head>
    <body>
      <div class="card">
        <h1>Bean Board Family</h1>
        <p>Sign up for exclusive offers, secret menu items, and a special treat!</p>
        <input type="text" placeholder="Full Name" />
        <input type="tel" placeholder="WhatsApp Number" />
        <button onclick="alert('Welcome to Bean Board!')">Join Now</button>
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
                        "**Colour palette applied to workspace:**\n\n"
                        "- **Primary (teal) `#28B4C4`**: buttons, active tabs, CTAs\n"
                        "- **Secondary (coffee brown) `#5C2318`**: text headings & contrast elements\n"
                        "- **Background cream `#FFF8ED`**: clean coastal layout\n\n"
                        "I have built the live interactive application in your right viewport. Type below to edit, build features, or publish."
                    )
                }
            ],
        }
    ]

# ---------------------------------------------------------
# Left Sidebar Navigation
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
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <a class="nav-item" href="#">➕ New Repl</a>
        <a class="nav-item" href="#">📥 Import</a>
        <a class="nav-item" href="#">📁 Projects</a>
        <a class="nav-item" href="#">⏱️ Routines <span style="background:#283347; font-size:0.7rem; padding:1px 5px; border-radius:4px; margin-left:auto; color:#60A5FA;">Beta</span></a>
        <a class="nav-item" href="#">📚 Library</a>
        <a class="nav-item" href="#">🔌 Integrations</a>
        <a class="nav-item" href="#">🔒 Security</a>
        """,
        unsafe_allow_html=True,
    )

    st.caption("RECENT")
    st.markdown(
        f"""
        <a class="nav-item" href="#" style="background:#1B2230; color:#FFFFFF;">› {st.session_state.project_name}</a>
        <a class="nav-item" href="#">› Fashion Showcase</a>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="upgrade-box">
            <div style="font-size:0.85rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
            <div style="font-size:0.75rem; color:#94A3B8;">Unlock unlimited GPU & model credits</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f"👤 **{st.session_state.user_name}**")

# ---------------------------------------------------------
# Top Action Header
# ---------------------------------------------------------
h_left, h_right = st.columns([5, 5])

with h_left:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:10px;">
            <div class="project-pill">🏷️ {st.session_state.project_name} ▾</div>
            <span style="font-size:0.85rem; color:#94A3B8; font-weight:600;">Design</span>
            <span style="font-size:0.85rem; color:#F26522; font-weight:700; border-bottom:2px solid #F26522; padding-bottom:2px;">Build</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with h_right:
    btn_c1, btn_c2, btn_c3 = st.columns([2, 2, 2])
    with btn_c1:
        st.button("⚙️ Tools", use_container_width=True)
    with btn_c2:
        st.button("👥 Invite", use_container_width=True)
    with btn_c3:
        st.markdown('<div class="publish-btn">', unsafe_allow_html=True)
        if st.button("🚀 Publish", use_container_width=True):
            st.toast("Application published to https://ciwi.replit.dev!", icon="🚀")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Split Panels: Chat Terminal (Left) & Browser Preview (Right)
# ---------------------------------------------------------
left_panel, right_panel = st.columns([1, 1], gap="medium")

# --- Left Panel: Terminal & Interaction ---
with left_panel:
    chat_container = st.container(height=520)
    with chat_container:
        for msg in st.session_state.messages:
            role = "assistant" if msg["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(msg["parts"][0]["text"])

    # Bottom-pinned prompt bar
    if prompt := st.chat_input("Message Agent..."):
        st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})
        
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            st.error("Please add GEMINI_API_KEY to your Streamlit secrets.")
        else:
            client = genai.Client(api_key=api_key)
            with left_panel:
                with st.spinner("⚡ Ciwi Agent is coding & deploying live..."):
                    gen_prompt = (
                        f"You are the Ciwi Autonomous Web Agent. The user wants: '{prompt}'.\n"
                        "Current app code is:\n"
                        f"{st.session_state.html_code}\n\n"
                        "Instructions:\n"
                        "1. Provide a concise bullet-point summary of what changed (colors, components, logic).\n"
                        "2. Provide the complete updated standalone HTML/CSS/JS inside a ```html ``` block."
                    )
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=gen_prompt,
                    )
                    resp_text = response.text

                    # Extract HTML to update the right-side preview
                    if "```html" in resp_text:
                        parsed_html = resp_text.split("```html")[1].split("```")[0].strip()
                        st.session_state.html_code = parsed_html

                    st.session_state.messages.append({"role": "model", "parts": [{"text": resp_text}]})
                    st.rerun()

# --- Right Panel: Browser Live Preview ---
with right_panel:
    st.markdown(
        f"""
        <div class="browser-frame">
            <div class="browser-toolbar">
                <div class="browser-dots">
                    <div class="dot" style="background:#EF4444;"></div>
                    <div class="dot" style="background:#F59E0B;"></div>
                    <div class="dot" style="background:#10B981;"></div>
                </div>
                <div class="browser-url-bar">[https://ciwi.replit.dev/](https://ciwi.replit.dev/){st.session_state.project_name.lower().replace(' ', '-')}</div>
                <span style="font-size:0.75rem; color:#94A3B8;">⟳</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Render interactive live application inside the frame
    components.html(st.session_state.html_code, height=520, scrolling=True)

    st.markdown("</div>", unsafe_allow_html=True)
