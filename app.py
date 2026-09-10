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
    /* Obsidian Canvas */
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #EDEDED !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 100% !important;
        padding: 1.5rem 2.8rem 2rem 2.8rem !important;
    }

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1C222E !important;
        padding-top: 0.6rem !important;
    }

    .sb-top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0.6rem 1rem 0.6rem;
    }

    .sb-top-icons {
        display: flex;
        align-items: center;
        gap: 14px;
        color: #8B949E;
    }

    .sb-workspace-dropdown {
        background: #181D27;
        border: 1px solid #232B39;
        border-radius: 8px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        gap: 9px;
        margin-bottom: 0.9rem;
        cursor: pointer;
    }

    .sb-workspace-dropdown img {
        width: 22px;
        height: 22px;
        border-radius: 50%;
    }

    .sb-new-btn {
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
        margin-bottom: 0.7rem;
        cursor: pointer;
    }

    .sb-menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 7px 10px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        cursor: pointer;
        transition: background 0.15s, color 0.15s;
    }

    .sb-menu-item:hover {
        background: #181E29;
        color: #FFFFFF;
    }

    .sb-menu-item svg {
        width: 17px;
        height: 17px;
        stroke: currentColor;
        stroke-width: 1.8;
        fill: none;
    }

    .beta-badge {
        background: #19273D;
        color: #38BDF8;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
        margin-left: auto;
    }

    .sb-section-label {
        font-size: 0.74rem;
        font-weight: 600;
        color: #64748B;
        padding: 1.2rem 0.6rem 0.4rem 0.6rem;
    }

    .sb-upgrade-box {
        background: #151A24;
        border: 1px solid #232B39;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.6rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .sb-upgrade-btn {
        background: #0070F3;
        width: 30px;
        height: 30px;
        border-radius: 7px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
    }

    .sb-user-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 0.4rem 0.2rem 0.4rem;
        margin-top: 0.8rem;
        border-top: 1px solid #1C222E;
    }

    /* Ambient Glow & Center Section */
    .glow-wrap {
        position: relative;
        max-width: 860px;
        margin: 2rem auto 0 auto;
    }

    .glow-bg {
        position: absolute;
        width: 780px;
        height: 280px;
        bottom: -30px;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(ellipse at center, rgba(175, 65, 20, 0.24) 0%, rgba(14, 17, 23, 0) 72%);
        pointer-events: none;
        z-index: 0;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #F8FAFC;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }

    /* Replit Custom 2-Row Search Bar */
    .replit-console {
        background: #141822;
        border: 1px solid #242D3D;
        border-radius: 14px;
        padding: 1rem 1.1rem 0.75rem 1.1rem;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.55);
        position: relative;
        z-index: 2;
        transition: border-color 0.2s ease;
    }

    .replit-console:focus-within {
        border-color: #F26522;
    }

    .replit-console input {
        width: 100%;
        background: transparent;
        border: none;
        outline: none;
        font-size: 1rem;
        color: #EDEDED;
        padding: 0 0 1.2rem 0;
    }

    .replit-console input::placeholder {
        color: #64748B;
    }

    .console-bottom-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #1A212E;
        padding-top: 0.65rem;
    }

    .console-tool-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: #1A212E;
        border: 1px solid #273244;
        border-radius: 6px;
        padding: 3px 9px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #CBD5E1;
        cursor: pointer;
    }

    .action-icon {
        color: #8B949E;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: color 0.15s;
    }

    .action-icon:hover {
        color: #FFFFFF;
    }

    /* Hide standard form decorations */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
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
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "home"
if "html_code" not in st.session_state:
    st.session_state.html_code = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------------
# Sidebar Component
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <!-- Header logo & icons -->
        <div class="sb-top-header">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522">
                <path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/>
            </svg>
            <div class="sb-top-icons">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>
            </div>
        </div>

        <!-- Personal workspace dropdown -->
        <div class="sb-workspace-dropdown">
            <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Mahesh" />
            <span style="font-size:0.86rem; font-weight:600; color:#E2E8F0;">Personal workspace</span>
            <svg style="margin-left:auto;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8B949E" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
        </div>

        <!-- + New Button -->
        <div class="sb-new-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v8m-4-4h8"/></svg>
            <span>New</span>
        </div>

        <!-- Nav Items -->
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            <span>Import</span>
        </div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><rect width="13" height="13" x="9" y="9" rx="2"/><rect width="13" height="13" x="2" y="2" rx="2"/></svg>
            <span>Projects</span>
        </div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>Routines</span>
            <span class="beta-badge">Beta</span>
        </div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10M6 10h10"/></svg>
            <span>Library</span>
        </div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
            <span>Integrations</span>
        </div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
            <span>Security</span>
        </div>

        <div class="sb-section-label">Recent</div>
        <div class="sb-menu-item">
            <svg viewBox="0 0 24 24"><rect width="13" height="13" x="9" y="9" rx="2"/><rect width="13" height="13" x="2" y="2" rx="2"/></svg>
            <span>Fashion Showcase</span>
        </div>
        <div class="sb-menu-item" style="color:#FFFFFF; background:#181E29;">
            <svg viewBox="0 0 24 24"><rect width="13" height="13" x="9" y="9" rx="2"/><rect width="13" height="13" x="2" y="2" rx="2"/></svg>
            <span>Dine Easy</span>
        </div>

        <!-- Upgrade Box -->
        <div class="sb-upgrade-box">
            <div>
                <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
                <div style="font-size:0.72rem; color:#8B949E; margin-top:2px;">Unlock more credits</div>
            </div>
            <div class="sb-upgrade-btn">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="#FFFFFF"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"/></svg>
            </div>
        </div>

        <div style="margin-top:1.2rem;">
            <div class="sb-menu-item">
                <svg viewBox="0 0 24 24"><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><circle cx="12" cy="17" r=".5"/></svg>
                <span>Learn more</span>
            </div>
        </div>

        <!-- User footer -->
        <div class="sb-user-footer">
            <div style="display:flex; align-items:center; gap:9px;">
                <img src="https://api.dicebear.com/7.x/bottts/svg?seed=Mahesh" style="width:22px; height:22px; border-radius:50%;" />
                <span style="font-size:0.88rem; font-weight:600; color:#FFFFFF;">Mahesh</span>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# View 1: Replit Exact Search Console
# ---------------------------------------------------------
if st.session_state.view_mode == "home":
    # Recent Cards Row
    st.markdown('<div style="font-size:0.84rem; font-weight:600; color:#8B949E; margin-bottom:0.75rem;">Recent projects</div>', unsafe_allow_html=True)
    c1, c2, c_rest = st.columns([1.8, 1.8, 6.4])
    with c1:
        st.markdown(
            """
            <div style="background:#131722; border:1px solid #202736; border-radius:12px; padding:0.9rem 1.2rem; cursor:pointer;">
                <div style="font-size:0.92rem; font-weight:600; color:#FFFFFF;">Fashion Showcase</div>
                <div style="font-size:0.76rem; color:#64748B; margin-top:3px;">🔒 · 11 minutes ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div style="background:#131722; border:1px solid #202736; border-radius:12px; padding:0.9rem 1.2rem; cursor:pointer;">
                <div style="font-size:0.92rem; font-weight:600; color:#FFFFFF;">Dine Easy</div>
                <div style="font-size:0.76rem; color:#64748B; margin-top:3px;">🔒 · 3 months ago</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Ambient Background & Headline
    st.markdown(
        f"""
        <div class="glow-wrap">
            <div class="glow-bg"></div>
            <div class="hero-title">{st.session_state.user_name}, what are we working on today?</div>
            <div style="font-size:0.8rem; color:#8B949E; margin-bottom:0.75rem; display:flex; align-items:center; gap:6px;">
                <span>Suggested for you</span>
                <span>⟳</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Suggestions Row
    s1, s2, s_rest = st.columns([2.4, 2.4, 5.2])
    trigger_prompt = None
    with s1:
        if st.button("✨ Help me get things done", use_container_width=True):
            trigger_prompt = "Build an analytics conversion dashboard with interactive filters"
    with s2:
        if st.button("↪ Review Resend delivery", use_container_width=True):
            trigger_prompt = "Build a transactional email monitor and resend webhook dashboard"

    # Search Bar Console
    with st.form("prompt_form", clear_on_submit=False):
        prompt_val = st.text_input(
            "Task",
            placeholder="Start chatting or describe a task...",
            label_visibility="collapsed",
        )
        
        # Bottom Console Toolbar matching Screenshot
        st.markdown(
            """
            <div class="console-bottom-toolbar">
                <div class="action-icon">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 5v14m-7-7h14"/></svg>
                </div>
                <div style="display:flex; align-items:center; gap:16px;">
                    <div class="console-tool-pill">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><circle cx="4" cy="4" r="2"/><circle cx="12" cy="4" r="2"/><circle cx="20" cy="4" r="2"/><circle cx="4" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="20" cy="12" r="2"/><circle cx="4" cy="20" r="2"/><circle cx="12" cy="20" r="2"/><circle cx="20" cy="20" r="2"/></svg>
                        <span>Free</span>
                        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
                    </div>
                    <div class="action-icon">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_space, col_send = st.columns([15, 1])
        with col_send:
            submitted = st.form_submit_button("↑")

    # Execution Handler
    active_query = prompt_val if submitted and prompt_val else trigger_prompt
    if active_query:
        api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
        if not api_key:
            st.error("Add GEMINI_API_KEY to Secrets.")
        else:
            client = genai.Client(api_key=api_key)
            st.session_state.view_mode = "workspace"
            st.session_state.messages.append({"role": "user", "parts": [{"text": active_query}]})

            with st.spinner("⚡ Autonomous Agent composing application..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Build an interactive web application for: '{active_query}'.\n"
                        "1. Provide a bulleted summary of UI components and colors.\n"
                        "2. Provide complete standalone HTML/CSS/JS inside a ```html ``` block."
                    ),
                )
                output = res.text
                if "```html" in output:
                    st.session_state.html_code = output.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

# ---------------------------------------------------------
# View 2: Split Workspace with Live Project Viewport
# ---------------------------------------------------------
else:
    # Top Bar Header
    th_l, th_r = st.columns([6, 4])
    with th_l:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="background:#181E29; border:1px solid #252F42; border-radius:8px; padding:4px 12px; font-weight:700; font-size:0.88rem; color:#FFFFFF;">
                    📁 Dine Easy ▾
                </div>
                <span style="color:#8B949E; font-size:0.85rem; font-weight:600;">Design</span>
                <span style="color:#F26522; font-size:0.85rem; font-weight:700; border-bottom:2px solid #F26522; padding-bottom:2px;">Build</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with th_r:
        b1, b2, b3 = st.columns([1, 1, 1.2])
        with b1:
            st.button("⚙️ Tools", use_container_width=True)
        with b2:
            st.button("👥 Invite", use_container_width=True)
        with b3:
            if st.button("🚀 Publish", use_container_width=True):
                st.toast("Published directly to ciwi.replit.dev!", icon="🚀")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # 50/50 Split Viewport
    col_term, col_slide = st.columns([1, 1], gap="medium")

    with col_term:
        chat_box = st.container(height=540)
        with chat_box:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["parts"][0]["text"])

        if user_msg := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "parts": [{"text": user_msg}]})
            api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
            client = genai.Client(api_key=api_key)

            with st.spinner("⚡ Updating workspace..."):
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Current code:\n{st.session_state.html_code}\n\n"
                        f"User request: {user_msg}\n"
                        "Return brief explanation + updated code in ```html ``` block."
                    ),
                )
                output = res.text
                if "```html" in output:
                    st.session_state.html_code = output.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "parts": [{"text": output}]})
                st.rerun()

    with col_slide:
        st.markdown(
            """
            <div style="background:#161B24; border:1px solid #262E3E; border-radius:12px 12px 0 0; padding:0.5rem 0.8rem; display:flex; align-items:center; gap:8px;">
                <div style="background:#0E1117; border:1px solid #262E3E; border-radius:6px; padding:3px 10px; font-size:0.78rem; color:#CBD5E1;">
                    Dine Easy ✕
                </div>
                <div style="background:#0E1117; border:1px solid #262E3E; border-radius:6px; padding:3px 10px; font-size:0.78rem; color:#8B949E; flex-grow:1; font-family:monospace;">
                    https://ciwi.replit.dev/dine-easy
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        components.html(st.session_state.html_code, height=520, scrolling=True)
