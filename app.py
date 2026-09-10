import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Replit - Workspace",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Exact Replit Dark Aesthetic CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Base */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #F0F6FC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        overflow-x: hidden;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2.5rem 2rem 2.5rem !important;
    }

    /* Sidebar Exact Clone */
    [data-testid="stSidebar"] {
        background-color: #12161F !important;
        border-right: 1px solid #1C2331 !important;
        padding-top: 0.8rem !important;
    }

    [data-testid="stSidebar"] * {
        color: #94A3B8 !important;
    }

    .sb-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.6rem 1rem 0.6rem;
    }

    .sb-logo {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .sb-logo svg {
        width: 22px;
        height: 22px;
        fill: #F26522;
    }

    .workspace-pill {
        background: #181E29;
        border: 1px solid #252F42;
        border-radius: 8px;
        padding: 0.5rem 0.75rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #E2E8F0 !important;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }

    .sb-nav-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.45rem 0.65rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8 !important;
        text-decoration: none;
        margin-bottom: 2px;
    }

    .sb-nav-item:hover {
        background: #1B2230;
        color: #FFFFFF !important;
    }

    .beta-tag {
        background: #1E283A;
        color: #60A5FA !important;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
        margin-left: auto;
    }

    .sb-recent-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B !important;
        margin: 1.6rem 0 0.5rem 0.6rem;
        letter-spacing: 0.04em;
    }

    .upgrade-card {
        background: #151B26;
        border: 1px solid #232E42;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 2.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .upgrade-btn-plus {
        background: #0070F3;
        color: #FFFFFF !important;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.1rem;
    }

    .user-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0.5rem 0.5rem 0.5rem;
        margin-top: 1rem;
        border-top: 1px solid #1C2331;
    }

    /* Main Center Hero */
    .recent-header-text {
        font-size: 0.82rem;
        font-weight: 600;
        color: #94A3B8;
        margin-bottom: 0.8rem;
    }

    .recent-cards-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 4.5rem;
    }

    .project-card {
        background: #131722;
        border: 1px solid #202736;
        border-radius: 12px;
        padding: 1rem 1.4rem;
        width: 220px;
        transition: border-color 0.2s;
        cursor: pointer;
    }

    .project-card:hover {
        border-color: #35425C;
    }

    .project-card-title {
        font-size: 0.92rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 0.35rem;
    }

    .project-card-sub {
        font-size: 0.78rem;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Radial Ambient Background Glow */
    .hero-glow-container {
        position: relative;
        text-align: left;
        max-width: 820px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    .hero-glow-bg {
        position: absolute;
        width: 700px;
        height: 350px;
        bottom: -40px;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(ellipse at center, rgba(168, 60, 20, 0.22) 0%, rgba(14, 17, 23, 0) 70%);
        pointer-events: none;
        z-index: 0;
    }

    .hero-headline {
        font-size: 2.7rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #F8FAFC;
        margin-bottom: 1.6rem;
        position: relative;
        z-index: 1;
    }

    .suggested-label {
        font-size: 0.8rem;
        color: #8B949E;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 6px;
        position: relative;
        z-index: 1;
    }

    .suggestion-pills {
        display: flex;
        gap: 0.6rem;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }

    /* Streamlit Buttons into Clean Dark Pills */
    div.stButton > button {
        background-color: #171B24 !important;
        color: #D1D5DB !important;
        border: 1px solid #262E3D !important;
        border-radius: 8px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 0.85rem !important;
    }

    div.stButton > button:hover {
        background-color: #212836 !important;
        border-color: #3B475C !important;
        color: #FFFFFF !important;
    }

    /* Prompt Input Capsule */
    [data-testid="stChatInput"] {
        background-color: #151922 !important;
        border: 1.5px solid #262E3E !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
        position: relative;
        z-index: 2;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #F26522 !important;
    }

    [data-testid="stChatInput"] textarea {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stBottomBlockContainer"] {
        background: transparent !important;
    }

    /* Split Screen Browser Window */
    .viewport-window {
        background: #FFFFFF;
        border: 1px solid #262E3E;
        border-radius: 12px;
        overflow: hidden;
        height: 82vh;
        display: flex;
        flex-direction: column;
    }

    .viewport-browser-bar {
        background: #161B24;
        border-bottom: 1px solid #262E3E;
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
        border: 1px solid #262E3E;
        border-radius: 6px;
        padding: 3px 10px;
        font-size: 0.78rem;
        color: #CBD5E1;
    }

    .browser-address-bar {
        background: #0E1117;
        border: 1px solid #262E3E;
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
if "workspace_view" not in st.session_state:
    st.session_state.workspace_view = "home"  # 'home' or 'workspace'
if "html_code" not in st.session_state:
    st.session_state.html_code = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sb-top">
            <div class="sb-logo">
                <svg viewBox="0 0 32 32"><path d="M7 6h8v8H7zm10 0h8v8h-8zM7 16h8v8H7z"/></svg>
            </div>
            <div style="display:flex; gap:10px; color:#94A3B8; font-size:0.9rem;">
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
        <a class="sb-nav-item" href="#">➕ New</a>
        <a class="sb-nav-item" href="#">📥 Import</a>
        <a class="sb-nav-item" href="#">📁 Projects</a>
        <a class="sb-nav-item" href="#">⏱️ Routines <span class="beta-tag">Beta</span></a>
        <a class="sb-nav-item" href="#">📚 Library</a>
        <a class="sb-nav-item" href="#">🔌 Integrations</a>
        <a class="sb-nav-item" href="#">🔒 Security</a>
        <div class="sb-recent-title">Recent</div>
        <a class="sb-nav-item" href="#">› Fashion Showcase</a>
        <a class="sb-nav-item" href="#" style="color:#FFFFFF !important; background:#181E29;">› Dine Easy</a>
        <div class="upgrade-card">
            <div>
                <div style="font-size:0.82rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
                <div style="font-size:0.72rem; color:#8B949E; margin-top:2px;">Unlock more credits</div>
            </div>
            <div class="upgrade-btn-plus">+</div>
        </div>
        <div style="margin-top:1.5rem;">
            <a class="sb-nav-item" href="#">❔ Learn more</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="user-footer">
            <div style="display:flex; align-items:center; gap:8px; color:#FFFFFF; font-size:0.88rem; font-weight:600;">
                <span>👤</span>
                <span>{st.session_state.user_name}</span>
            </div>
            <span style="color:#64748B; cursor:pointer;">⚙️</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# View 1: Replit Exact Home Screen (Screenshot Match)
# ---------------------------------------------------------
if st.session_state.workspace_view == "home":
    # Recent Projects Cards Row
    st.markdown('<div class="recent-header-text">Recent projects</div>', unsafe_allow_html=True)
    
    r_col1, r_col2, r_col_rest = st.columns([1.8, 1.8, 6.4])
    with r_col1:
        st.markdown(
            """
            <div class="project-card">
                <div class="project-card-title">Fashion Showcase</div>
                <div class="project-card-sub">🔒 · 11 minutes ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r_col2:
        st.markdown(
            """
            <div class="project-card">
                <div class="project-card-title">Dine Easy</div>
                <div class="project-card-sub">🔒 · 3 months ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Hero Center with Ambient Glow
    st.markdown(
        f"""
        <div class="hero-glow-container">
            <div class="hero-glow-bg"></div>
            <div class="hero-headline">{st.session_state.user_name}, what are we working on today?</div>
            <div class="suggested-label">
                <span>Suggested for you</span>
                <span style="cursor:pointer;">⟳</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Suggestion Pills
    pill_c1, pill_c2, pill_rest = st.columns([2.2, 2.2, 5.6])
    selected_preset = None
    with pill_c1:
        if st.button("✨ Help me get things done", use_container_width=True):
            selected_preset = "Build a customer feedback dashboard with analytical metrics and graphs."
    with pill_c2:
        if st.button("↪ Review Resend delivery", use_container_width=True):
            selected_preset = "Build an email delivery log and newsletter analytics app."

    # Bottom Pinned Prompt Capsule
    prompt = st.chat_input("Start chatting or describe a task...") or selected_preset

    if prompt:
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            st.error("Please configure your GEMINI_API_KEY in Streamlit Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            st.session_state.workspace_view = "workspace"
            st.session_state.messages.append({"role": "user", "parts": [{"text": prompt}]})

            with st.spinner("⚡ Ciwi Agent is building your application..."):
                system_instruction = (
                    "You are the Ciwi Autonomous Web Agent (Replit Agent clone). "
                    "1. Explain the changes and design tokens concisely in markdown bullet points. "
                    "2. Return the complete, fully responsive standalone HTML/CSS/JS code wrapped in a ```html ``` block."
                )
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=0.7),
                )
                raw_text = res.text

                if "```html" in raw_text:
                    st.session_state.html_code = raw_text.split("```html")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    st.session_state.html_code = raw_text.split("```")[1].split("```")[0].strip()
                else:
                    st.session_state.html_code = f"<html><body style='font-family:sans-serif;padding:2rem;'><h1>Live Build</h1><p>{raw_text}</p></body></html>"

                st.session_state.messages.append({"role": "model", "parts": [{"text": raw_text}]})
                st.rerun()

# ---------------------------------------------------------
# View 2: Replit 2-Column Split Workspace (Terminal + Live Slide)
# ---------------------------------------------------------
else:
    # Workspace Top Header Bar
    top_l, top_r = st.columns([6, 4])
    with top_l:
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="background:#181E29; border:1px solid #252F42; border-radius:8px; padding:4px 12px; font-weight:700; font-size:0.88rem; color:#FFFFFF;">
                    📁 {st.session_state.project_name} ▾
                </div>
                <span style="color:#94A3B8; font-size:0.85rem; font-weight:600; cursor:pointer;">Design</span>
                <span style="color:#F26522; font-size:0.85rem; font-weight:700; border-bottom: 2px solid #F26522; padding-bottom: 2px;">Build</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top_r:
        b1, b2, b3 = st.columns([1, 1, 1.3])
        with b1:
            st.button("⚙️ Tools", use_container_width=True)
        with b2:
            st.button("👥 Invite", use_container_width=True)
        with b3:
            if st.button("🚀 Publish", use_container_width=True):
                st.toast("Application deployed to ciwi.replit.dev!", icon="🚀")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 50/50 Split
    col_term, col_view = st.columns([1, 1], gap="medium")

    # Left: Terminal Output & Chat
    with col_term:
        chat_container = st.container(height=540)
        with chat_container:
            for msg in st.session_state.messages:
                role = "assistant" if msg["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(msg["parts"][0]["text"])

        # Pinned message input
        if follow_up := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "parts": [{"text": follow_up}]})
            api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            client = genai.Client(api_key=api_key)

            with st.spinner("⚡ Updating live workspace..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Current code:\n{st.session_state.html_code}\n\n"
                        f"User request: {follow_up}\n"
                        "Return concise summary + full code inside ```html ``` block."
                    ),
                )
                output = res.text
                if "```html" in output:
                    st.session_state.html_code = output.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

    # Right: The Live Project Slide Viewport
    with col_view:
        st.markdown(
            f"""
            <div class="viewport-window">
                <div class="viewport-browser-bar">
                    <div class="browser-tabs">
                        <span>{st.session_state.project_name}</span>
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

        components.html(st.session_state.html_code, height=540, scrolling=True)

        st.markdown("</div>", unsafe_allow_html=True)
