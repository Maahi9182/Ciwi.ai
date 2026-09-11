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

# --- Theme CSS (Beige & Orange) ---
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #FBF8F3 !important;
        background-image: radial-gradient(ellipse 70% 45% at 50% 92%, rgba(242, 101, 34, 0.12) 0%, rgba(251, 248, 243, 0) 75%) !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        color: #1F2937 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 1080px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        margin: 0 auto !important;
    }

    [data-testid="stSidebar"] {
        background-color: #F5EFEB !important;
        border-right: 1px solid #E5DCD0 !important;
        padding-top: 0.6rem !important;
    }

    .sb-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.4rem 0.8rem 0.4rem;
    }

    .workspace-pill {
        background: #ECE3D8;
        border: 1px solid #DFD4C5;
        border-radius: 8px;
        padding: 6px 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #2D3748;
        font-size: 0.86rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #4B5563 !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 0.4rem 0.6rem !important;
        width: 100% !important;
        box-shadow: none !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #ECE3D8 !important;
        color: #111827 !important;
    }

    .upgrade-box {
        background: #EDE4D8;
        border: 1px solid #DFD4C5;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.2rem;
    }

    .progress-bar-bg {
        background: #DFD4C5;
        border-radius: 999px;
        height: 4px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }

    .progress-bar-fill {
        background: #F26522;
        height: 100%;
        width: 100%;
    }

    .import-card {
        background: #FFFFFF;
        border: 1px solid #E8DFD3;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        transition: border-color 0.15s, transform 0.15s;
    }

    .import-card:hover {
        border-color: #F26522;
        transform: translateY(-1px);
    }

    .project-preview-card {
        background: #FFFFFF;
        border: 1px solid #E8DFD3;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }

    .preview-thumb {
        height: 140px;
        background: #F7F2EA;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid #E8DFD3;
        font-size: 2rem;
    }

    .preview-footer {
        padding: 0.9rem 1.1rem;
    }

    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5DCD0 !important;
        border-radius: 9999px !important;
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        padding: 0.4rem 1.1rem !important;
        display: inline-flex !important;
        align-items: center !important;
        margin-bottom: 0.3rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    div.stButton > button:hover {
        background-color: #FFFDF9 !important;
        border-color: #F26522 !important;
        color: #F26522 !important;
    }

    [data-testid="stForm"] {
        background-color: #FFFFFF !important;
        border: 1.5px solid #E8DFD3 !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem 0.65rem 1.1rem !important;
        box-shadow: 0 8px 24px rgba(242, 101, 34, 0.06) !important;
        position: relative !important;
        margin-top: 0.6rem !important;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #F26522 !important;
        box-shadow: 0 8px 28px rgba(242, 101, 34, 0.14) !important;
    }

    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        color: #1F2937 !important;
        padding: 0.1rem 0 1rem 0 !important;
    }

    [data-testid="stForm"] input::placeholder {
        color: #9CA3AF !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: #F26522 !important;
        border: none !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        padding: 0 !important;
        min-width: 28px !important;
        width: 28px !important;
        height: 28px !important;
        border-radius: 50% !important;
        position: absolute !important;
        right: 1.1rem !important;
        bottom: 0.65rem !important;
        z-index: 10 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 6px rgba(242, 101, 34, 0.3) !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background: #DC5416 !important;
        transform: scale(1.05);
    }

    .console-bottom-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #F3ECE1;
        padding-top: 0.5rem;
    }

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD3 !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
    }

    [data-testid="stChatMessage"] * {
        color: #1F2937 !important;
    }

    .btn-upgrade-orange {
        background: #F26522;
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
        box-shadow: 0 2px 8px rgba(242, 101, 34, 0.25);
    }

    .btn-upgrade-orange:hover {
        background: #DC5416;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- State ---
if "user_name" not in st.session_state:
    st.session_state.user_name = "Mahesh"
if "current_nav" not in st.session_state:
    st.session_state.current_nav = "Home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "html_code" not in st.session_state:
    st.session_state.html_code = ""

def is_design_task(text: str) -> bool:
    keywords = ["build", "create", "make a website", "make an app", "design", "redesign", "add button", "clone", "dashboard", "html", "css"]
    return any(k in text.lower() for k in keywords)

def query_gemini(prompt: str, is_design: bool):
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        return "Missing GEMINI_API_KEY in Secrets."
    client = genai.Client(api_key=api_key)

    if is_design:
        sys_prompt = (
            "You are Ciwi, an autonomous web-building AI. "
            "1. Give a concise summary of changes in bullet points. "
            "2. Provide complete standalone HTML/CSS/JS inside a ```html block."
        )
        context = f"Current App Code:\n{st.session_state.html_code}\n\nTask: {prompt}"
    else:
        sys_prompt = "You are Ciwi, a helpful AI assistant. Provide concise, friendly conversation. Do NOT output code or HTML."
        context = prompt

    res = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=context,
        config=types.GenerateContentConfig(system_instruction=sys_prompt, temperature=0.7),
    )
    return res.text

# --- Left Sidebar ---
with st.sidebar:
    st.markdown(
        """
        <div class="sb-header">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="#F26522"><path d="M4 4h6v6H4zm10 0h6v6h-6zM4 14h6v6H4z"/></svg>
            <div style="display:flex; gap:12px; color:#6B7280; font-size: 0.95rem;">
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
        """,
        unsafe_allow_html=True,
    )

    if st.button("➕  New", key="nav_new"):
        st.session_state.current_nav = "Home"
        st.session_state.messages = []
        st.rerun()

    if st.button("📥  Import", key="nav_import"):
        st.session_state.current_nav = "Import"
        st.rerun()

    if st.button("📁  Projects", key="nav_projects"):
        st.session_state.current_nav = "Projects"
        st.rerun()

    if st.button("⏱️  Routines  (Beta)", key="nav_routines"):
        st.session_state.current_nav = "Routines"
        st.rerun()

    if st.button("📚  Library", key="nav_library"):
        st.session_state.current_nav = "Library"
        st.rerun()

    if st.button("🔌  Integrations", key="nav_integrations"):
        st.session_state.current_nav = "Integrations"
        st.rerun()

    if st.button("🛡️  Security", key="nav_security"):
        st.session_state.current_nav = "Security"
        st.rerun()

    st.markdown("<div style='font-size:0.74rem; font-weight:700; color:#8C7B6B; padding:1.2rem 0.4rem 0.3rem 0.4rem;'>Recent</div>", unsafe_allow_html=True)
    if st.button("🗂️  Ciwi AI Assistant", key="rec_ciwi"):
        st.session_state.current_nav = "Home"
        st.rerun()
    if st.button("🗂️  Fashion Showcase", key="rec_fashion"):
        st.session_state.current_nav = "Home"
        st.rerun()
    if st.button("🗂️  Dine Easy", key="rec_dine"):
        st.session_state.current_nav = "Home"
        st.rerun()

    st.markdown(
        """
        <div class="upgrade-box">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.84rem; font-weight:700; color:#1F2937;">Upgrade your plan</div>
                    <div style="font-size:0.72rem; color:#6B7280; margin-top:2px;">Unlock more credits</div>
                </div>
                <div style="background:#F26522; border-radius:6px; width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#FFF; font-weight:700;">+</div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#6B7280; margin-top:8px;">
                <span>Free allowance</span>
                <span>100% used</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:1.2rem 0.4rem 0.2rem 0.4rem; border-top:1px solid #E5DCD0; margin-top:1.2rem;">
            <div style="display:flex; align-items:center; gap:8px; color:#1F2937; font-weight:600; font-size:0.88rem;">
                <span>👤</span>
                <span>Mahesh</span>
            </div>
            <span style="color:#8C7B6B; cursor:pointer;">⚙️</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Navigation Routing ---
if st.session_state.current_nav == "Home":
    clicked_task = None

    if not st.session_state.messages:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#6B7280; margin-bottom:0.75rem;">Recent projects</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown('<div class="import-card"><strong style="color:#1F2937;">Ciwi AI Assistant</strong><span style="color:#9CA3AF; font-size:0.76rem;">🔒 · 2m ago</span></div>', unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="import-card"><strong style="color:#1F2937;">Fashion Showcase</strong><span style="color:#9CA3AF; font-size:0.76rem;">🔒 · 53m ago</span></div>', unsafe_allow_html=True)
        with r3:
            st.markdown('<div class="import-card"><strong style="color:#1F2937;">Dine Easy</strong><span style="color:#9CA3AF; font-size:0.76rem;">🔒 · 3mo ago</span></div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 2.2rem;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem; font-weight:700; color:#111827; margin-bottom:1.4rem;">{st.session_state.user_name}, what are we working on today?</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem; color:#6B7280; margin-bottom:0.75rem;">Suggested for you ⟳</div>', unsafe_allow_html=True)

        if st.button("✦  Help me get things done", key="p_help"):
            clicked_task = "Build a productivity dashboard with task organization"
        if st.button("🟧  Review RevenueCat growth", key="p_rc"):
            clicked_task = "Build an analytics dashboard tracking RevenueCat MRR and subscribers"
        if st.button("📄  Turn my notes into a slide deck", key="p_deck"):
            clicked_task = "Build a presentation slide generator app from user notes"

    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "assistant" if msg["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(msg["text"])

    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.6rem; margin-bottom:0.6rem; font-size:0.86rem; color:#6B7280;">
            <span>You've used up your daily credits. Upgrade to continue.</span>
            <button class="btn-upgrade-orange">+ Upgrade to Core</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("home_search_form", clear_on_submit=True):
        typed_input = st.text_input("Task", placeholder="Start chatting or describe a task...", label_visibility="collapsed", key="home_search_input")
        st.markdown(
            """
            <div class="console-bottom-toolbar">
                <span style="color:#6B7280; font-size:1.15rem; cursor:pointer;">+</span>
                <div style="display:flex; align-items:center; gap:16px; margin-right: 36px;">
                    <div style="display:inline-flex; align-items:center; gap:5px; color:#4B5563; font-size:0.82rem; cursor:pointer;">
                        <span>:::</span> <span>Free ▾</span>
                    </div>
                    <span style="color:#6B7280; cursor:pointer; font-size:0.95rem;">🎙️</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("↑")

    active_prompt = typed_input if (submitted and typed_input) else clicked_task
    if active_prompt:
        st.session_state.messages.append({"role": "user", "text": active_prompt})
        if is_design_task(active_prompt):
            st.session_state.current_nav = "Workspace"
            with st.spinner("⚡ Composing application..."):
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

elif st.session_state.current_nav == "Import":
    st.markdown('<h1 style="font-size:2.2rem; font-weight:700; color:#111827; margin-bottom:0.4rem;">Import to Replit</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280; font-size:0.95rem; margin-bottom:1.8rem;">Migrate data, code, and designs from other apps into Replit</p>', unsafe_allow_html=True)

    import_options = [
        ("GitHub", "Import any repository or existing app. Agent may be less predictable.", "🐙"),
        ("Bitbucket", "Import a repository or existing app. Agent support may be limited.", "🔷"),
        ("Figma Design", "Convert your designs into live Apps using Replit Agent", "🎨"),
        ("Lovable FREE", "Migrate your site to make it production-ready", "🤍"),
        ("Bolt", "Migrate your prototype to make it production-ready", "⚡"),
        ("Base44 FREE", "Migrate your site to make it production-ready", "🌐"),
        ("Vercel FREE", "Migrate your site to make it production-ready", "▲"),
        ("Spreadsheet", "Create an app from Excel, CSV, or Google Sheets data", "📊"),
        ("Zip file", "Import from a .zip file.", "📦"),
        ("Empty", "Start from a completely empty project without Agent setup or scaffolding.", "📄"),
    ]

    for i in range(0, len(import_options), 2):
        col1, col2 = st.columns(2)
        with col1:
            title, desc, ico = import_options[i]
            st.markdown(f'<div class="import-card"><div style="display:flex; align-items:center; gap:12px;"><span style="font-size:1.5rem;">{ico}</span><div><div style="font-weight:700; color:#111827;">{title}</div><div style="font-size:0.78rem; color:#6B7280;">{desc}</div></div></div><span style="color:#9CA3AF;">→</span></div>', unsafe_allow_html=True)
        if i + 1 < len(import_options):
            with col2:
                title, desc, ico = import_options[i+1]
                st.markdown(f'<div class="import-card"><div style="display:flex; align-items:center; gap:12px;"><span style="font-size:1.5rem;">{ico}</span><div><div style="font-weight:700; color:#111827;">{title}</div><div style="font-size:0.78rem; color:#6B7280;">{desc}</div></div></div><span style="color:#9CA3AF;">→</span></div>', unsafe_allow_html=True)

elif st.session_state.current_nav == "Projects":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#111827; margin-bottom:1.2rem;">📁 Projects</h1>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([4, 2, 2, 2])
    with f1:
        st.text_input("Search projects", placeholder="Search projects...", label_visibility="collapsed")
    with f2:
        st.selectbox("Status", ["Any status", "Active", "Archived"], label_visibility="collapsed")
    with f3:
        st.selectbox("Artifact", ["Any artifact type", "Website", "Mobile App", "Backend"], label_visibility="collapsed")
    with f4:
        st.selectbox("View", ["All projects", "Shared with me"], label_visibility="collapsed")

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">🤖</div><div class="preview-footer"><strong style="color:#111827;">Ciwi AI Assistant</strong><div style="color:#6B7280; font-size:0.78rem;">🔒 · 25 minutes ago</div></div></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">👗</div><div class="preview-footer"><strong style="color:#111827;">Fashion Showcase</strong><div style="color:#6B7280; font-size:0.78rem;">🔒 · 1 hour ago</div></div></div>', unsafe_allow_html=True)
    with p_col3:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">☕</div><div class="preview-footer"><strong style="color:#111827;">Dine Easy</strong><div style="color:#6B7280; font-size:0.78rem;">🔒 · 1 hour ago</div></div></div>', unsafe_allow_html=True)

elif st.session_state.current_nav == "Routines":
    st.markdown('<h1 style="font-size:2.2rem; font-weight:700; color:#111827; margin-bottom:0.2rem;">⏱️ Routines <span style="background:#FFE6D8; color:#F26522; font-size:0.8rem; padding:2px 8px; border-radius:4px; font-weight:700;">Beta</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280; font-size:0.92rem;">Run Replit on a schedule</p>', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#111827; margin-top:2rem;">Put recurring work on autopilot</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color:#6B7280; font-size:0.88rem; margin-bottom:1.4rem;">Upgrade to Replit Core to schedule Agent tasks that run for you, even when you are away.</p>', unsafe_allow_html=True)

    routines_list = [
        ("📅 Check my calendar each morning and tell me what to prepare for", "↗"),
        ("✉️ Go through my inbox every couple of days and pull out emails that need a reply", "↗"),
        ("💬 Catch me up every Friday on the Slack messages I missed", "↗"),
        ("⏰ Schedule a custom routine that...", "↗")
    ]
    for text, arr in routines_list:
        st.markdown(f'<div class="import-card" style="margin-bottom:0.8rem;"><span style="color:#1F2937; font-size:0.9rem;">{text}</span><span style="color:#F26522; font-weight:bold;">{arr}</span></div>', unsafe_allow_html=True)

elif st.session_state.current_nav == "Library":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#111827; margin-bottom:0.2rem;">📚
