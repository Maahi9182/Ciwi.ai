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

# ---------------------------------------------------------
# Global Replit Dark Theme CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], .main {
        background-color: #0E1117 !important;
        color: #EDEDED !important;
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

    /* Left Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12151D !important;
        border-right: 1px solid #1C222E !important;
        padding-top: 0.6rem !important;
    }

    .sb-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.2rem 0.4rem 0.8rem 0.4rem;
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

    /* Sidebar buttons */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #94A3B8 !important;
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
        background-color: #181E29 !important;
        color: #FFFFFF !important;
    }

    .upgrade-box {
        background: #151A24;
        border: 1px solid #232B39;
        border-radius: 10px;
        padding: 0.85rem;
        margin-top: 1.2rem;
    }

    .progress-bar-bg {
        background: #232B39;
        border-radius: 999px;
        height: 4px;
        width: 100%;
        margin-top: 6px;
        overflow: hidden;
    }

    .progress-bar-fill {
        background: #0070F3;
        height: 100%;
        width: 100%;
    }

    /* Section Cards Grid */
    .grid-2col {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .grid-3col {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1rem;
        margin-top: 1.5rem;
    }

    .import-card {
        background: #141822;
        border: 1px solid #232B3A;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        cursor: pointer;
        transition: border-color 0.15s;
    }

    .import-card:hover {
        border-color: #38455B;
    }

    .import-card-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .project-preview-card {
        background: #141822;
        border: 1px solid #232B3A;
        border-radius: 12px;
        overflow: hidden;
    }

    .preview-thumb {
        height: 140px;
        background: #1C2230;
        display: flex;
        align-items: center;
        justify-content: center;
        border-bottom: 1px solid #232B3A;
        font-size: 2rem;
    }

    .preview-footer {
        padding: 0.9rem 1.1rem;
    }

    /* Replit Input Console */
    [data-testid="stForm"] {
        background-color: #141822 !important;
        border: 1px solid #262E3E !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.1rem 0.65rem 1.1rem !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5) !important;
        position: relative !important;
        margin-top: 0.6rem !important;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #3B475C !important;
    }

    [data-testid="stForm"] input {
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        font-size: 1rem !important;
        color: #FFFFFF !important;
        padding: 0.1rem 0 1rem 0 !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background: transparent !important;
        border: none !important;
        color: #7E8B9D !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        padding: 0 !important;
        min-width: 24px !important;
        width: 24px !important;
        height: 24px !important;
        box-shadow: none !important;
        position: absolute !important;
        right: 1.2rem !important;
        bottom: 0.75rem !important;
        z-index: 10 !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        color: #FFFFFF !important;
    }

    .console-bottom-toolbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-top: 1px solid #1C2330;
        padding-top: 0.5rem;
    }

    /* Chat Messages styling */
    [data-testid="stChatMessage"] {
        background-color: #141822 !important;
        border: 1px solid #232B3A !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stChatMessage"] * {
        color: #E6EDF3 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Initializations
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# Left Sidebar Navigation (Section by Section)
# ---------------------------------------------------------
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

    st.markdown("<div style='font-size:0.74rem; font-weight:700; color:#64748B; padding:1.2rem 0.4rem 0.3rem 0.4rem;'>Recent</div>", unsafe_allow_html=True)
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
                    <div style="font-size:0.84rem; font-weight:700; color:#FFFFFF;">Upgrade your plan</div>
                    <div style="font-size:0.72rem; color:#8B949E; margin-top:2px;">Unlock more credits</div>
                </div>
                <div style="background:#0070F3; border-radius:6px; width:26px; height:26px; display:flex; align-items:center; justify-content:center; color:#FFF; font-weight:700;">+</div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#8B949E; margin-top:8px;">
                <span>Free allowance</span>
                <span>100% used</span>
            </div>
            <div class="progress-bar-bg"><div class="progress-bar-fill"></div></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:1.2rem 0.4rem 0.2rem 0.4rem; border-top:1px solid #1C222E; margin-top:1.2rem;">
            <div style="display:flex; align-items:center; gap:8px; color:#FFFFFF; font-weight:600; font-size:0.88rem;">
                <span>👤</span>
                <span>Mahesh</span>
            </div>
            <span style="color:#64748B; cursor:pointer;">⚙️</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECTION 1: HOME (Dashboard + Search Bar + Chat)
# ---------------------------------------------------------
if st.session_state.current_nav == "Home":
    clicked_task = None

    if not st.session_state.messages:
        st.markdown('<div style="font-size:0.82rem; font-weight:600; color:#8B949E; margin-bottom:0.75rem;">Recent projects</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown('<div class="import-card"><strong style="color:#FFF;">Ciwi AI Assistant</strong><span style="color:#64748B; font-size:0.76rem;">🔒 · 2m ago</span></div>', unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="import-card"><strong style="color:#FFF;">Fashion Showcase</strong><span style="color:#64748B; font-size:0.76rem;">🔒 · 53m ago</span></div>', unsafe_allow_html=True)
        with r3:
            st.markdown('<div class="import-card"><strong style="color:#FFF;">Dine Easy</strong><span style="color:#64748B; font-size:0.76rem;">🔒 · 3mo ago</span></div>', unsafe_allow_html=True)

        st.markdown("<div style='height: 2.2rem;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:2.5rem; font-weight:600; color:#F3F4F6; margin-bottom:1.4rem;">{st.session_state.user_name}, what are we working on today?</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.8rem; color:#8C96A5; margin-bottom:0.75rem;">Suggested for you ⟳</div>', unsafe_allow_html=True)

        if st.button("✦  Help me get things done", key="p_help"):
            clicked_task = "Build a productivity dashboard with task organization"
        if st.button("🟥  Review RevenueCat growth", key="p_rc"):
            clicked_task = "Build an analytics dashboard tracking RevenueCat MRR and subscribers"
        if st.button("📄  Turn my notes into a slide deck", key="p_deck"):
            clicked_task = "Build a presentation slide generator app from user notes"

    # Chat Messages rendered ABOVE the search bar
    if st.session_state.messages:
        for msg in st.session_state.messages:
            role = "assistant" if msg["role"] == "model" else "user"
            with st.chat_message(role):
                st.markdown(msg["text"])

    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.6rem; margin-bottom:0.6rem; font-size:0.86rem; color:#94A3B8;">
            <span>You've used up your daily credits. Upgrade to continue.</span>
            <button style="background:#0070F3; color:#FFF; border:none; border-radius:8px; padding:6px 14px; font-weight:600; cursor:pointer;">+ Upgrade to Core</button>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Bottom search console
    with st.form("home_search_form", clear_on_submit=True):
        typed_input = st.text_input("Task", placeholder="Start chatting or describe a task...", label_visibility="collapsed", key="home_search_input")
        st.markdown(
            """
            <div class="console-bottom-toolbar">
                <span style="color:#7E8B9D; font-size:1.15rem; cursor:pointer;">+</span>
                <div style="display:flex; align-items:center; gap:16px; margin-right: 32px;">
                    <div style="display:inline-flex; align-items:center; gap:5px; color:#8E9BAE; font-size:0.82rem; cursor:pointer;">
                        <span>:::</span> <span>Free ▾</span>
                    </div>
                    <span style="color:#7E8B9D; cursor:pointer; font-size:0.95rem;">🎙️</span>
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

# ---------------------------------------------------------
# SECTION 2: IMPORT (/import)
# ---------------------------------------------------------
elif st.session_state.current_nav == "Import":
    st.markdown('<h1 style="font-size:2.2rem; font-weight:700; color:#FFF; margin-bottom:0.4rem;">Import to Replit</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:0.95rem; margin-bottom:1.8rem;">Migrate data, code, and designs from other apps into Replit</p>', unsafe_allow_html=True)

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
            st.markdown(f'<div class="import-card"><div class="import-card-left"><span style="font-size:1.5rem;">{ico}</span><div><div style="font-weight:700; color:#FFF;">{title}</div><div style="font-size:0.78rem; color:#8B949E;">{desc}</div></div></div><span style="color:#64748B;">→</span></div>', unsafe_allow_html=True)
        if i + 1 < len(import_options):
            with col2:
                title, desc, ico = import_options[i+1]
                st.markdown(f'<div class="import-card"><div class="import-card-left"><span style="font-size:1.5rem;">{ico}</span><div><div style="font-weight:700; color:#FFF;">{title}</div><div style="font-size:0.78rem; color:#8B949E;">{desc}</div></div></div><span style="color:#64748B;">→</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 3: PROJECTS (/repls)
# ---------------------------------------------------------
elif st.session_state.current_nav == "Projects":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#FFF; margin-bottom:1.2rem;">📁 Projects</h1>', unsafe_allow_html=True)
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
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">🤖</div><div class="preview-footer"><strong style="color:#FFF;">Ciwi AI Assistant</strong><div style="color:#8B949E; font-size:0.78rem;">🔒 · 25 minutes ago</div></div></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">👗</div><div class="preview-footer"><strong style="color:#FFF;">Fashion Showcase</strong><div style="color:#8B949E; font-size:0.78rem;">🔒 · 1 hour ago</div></div></div>', unsafe_allow_html=True)
    with p_col3:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">☕</div><div class="preview-footer"><strong style="color:#FFF;">Dine Easy</strong><div style="color:#8B949E; font-size:0.78rem;">🔒 · 1 hour ago</div></div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 4: ROUTINES (/routines)
# ---------------------------------------------------------
elif st.session_state.current_nav == "Routines":
    st.markdown('<h1 style="font-size:2.2rem; font-weight:700; color:#FFF; margin-bottom:0.2rem;">⏱️ Routines <span style="background:#19273D; color:#38BDF8; font-size:0.8rem; padding:2px 8px; border-radius:4px;">Beta</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:0.92rem;">Run Replit on a schedule</p>', unsafe_allow_html=True)
    st.markdown('<h4 style="color:#FFF; margin-top:2rem;">Put recurring work on autopilot</h4>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:0.88rem; margin-bottom:1.4rem;">Upgrade to Replit Core to schedule Agent tasks that run for you, even when you are away.</p>', unsafe_allow_html=True)

    routines_list = [
        ("📅 Check my calendar each morning and tell me what to prepare for", "↗"),
        ("✉️ Go through my inbox every couple of days and pull out emails that need a reply", "↗"),
        ("💬 Catch me up every Friday on the Slack messages I missed", "↗"),
        ("⏰ Schedule a custom routine that...", "↗")
    ]
    for text, arr in routines_list:
        st.markdown(f'<div class="import-card" style="margin-bottom:0.8rem;"><span style="color:#E2E8F0; font-size:0.9rem;">{text}</span><span style="color:#64748B;">{arr}</span></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 5: LIBRARY (/library)
# ---------------------------------------------------------
elif st.session_state.current_nav == "Library":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#FFF; margin-bottom:0.2rem;">📚 Library</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:0.92rem; margin-bottom:1.5rem;">Everything Replit has made across your projects</p>', unsafe_allow_html=True)
    l1, l2, l3 = st.columns([5, 2, 2])
    with l1:
        st.text_input("Search artifacts", placeholder="Search artifacts and assets", label_visibility="collapsed")
    with l2:
        st.selectbox("Type", ["Any type", "Code", "Components"], label_visibility="collapsed")
    with l3:
        st.selectbox("File", ["Any file type", "HTML", "JSON"], label_visibility="collapsed")

    lib1, lib2, lib3 = st.columns(3)
    with lib1:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">💻</div><div class="preview-footer"><strong style="color:#FFF;">Ciwi AI Assistant</strong><div style="color:#8B949E; font-size:0.75rem;">Website · 35m ago</div></div></div>', unsafe_allow_html=True)
    with lib2:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">🖼️</div><div class="preview-footer"><strong style="color:#FFF;">Aster Row</strong><div style="color:#8B949E; font-size:0.75rem;">Website · 1h ago</div></div></div>', unsafe_allow_html=True)
    with lib3:
        st.markdown('<div class="project-preview-card"><div class="preview-thumb">☕</div><div class="preview-footer"><strong style="color:#FFF;">Bean Board - Bheemili</strong><div style="color:#8B949E; font-size:0.75rem;">Website · 1h ago</div></div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SECTION 6: INTEGRATIONS & SETTINGS MODAL
# ---------------------------------------------------------
elif st.session_state.current_nav == "Integrations":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#FFF; margin-bottom:0.4rem;">⚙️ Settings & Integrations</h1>', unsafe_allow_html=True)
    tab_int, tab_custom = st.tabs(["🔌 Connected Integrations", "🧠 Customization & Memory"])

    with tab_int:
        st.markdown('<p style="color:#8B949E; font-size:0.9rem; margin-bottom:1.2rem;">Connect your favorite services for seamless workspace syncing.</p>', unsafe_allow_html=True)
        integrations_data = [
            ("Google Docs", "Connect to create, read, and update documents.", "📄"),
            ("Google Drive", "Connect to Google Drive to manage files.", "💾"),
            ("Google Sheets", "Read, write, and modify spreadsheet data via REST API.", "📊"),
            ("HubSpot", "Manage contacts, deals, and marketing campaigns.", "🎯"),
            ("Intercom", "Manage users and conversations in Intercom.", "💬"),
            ("Jira", "Issue tracking, project boards, and sprint logs.", "🔷"),
            ("Linear", "Query issues, cycles, and manage tracking via GraphQL.", "🟣"),
            ("Mailchimp", "Manage subscriber lists and campaigns.", "🐒"),
            ("Dropbox", "Sync files, assets, and backups.", "📦"),
        ]
        for idx in range(0, len(integrations_data), 3):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                t, d, ico = integrations_data[idx]
                st.markdown(f'<div class="import-card"><div><span style="font-size:1.4rem;">{ico}</span><div style="font-weight:700; color:#FFF; margin-top:6px;">{t}</div><div style="font-size:0.76rem; color:#8B949E; margin-bottom:8px;">{d}</div><button style="background:#1E2636; border:1px solid #2B3547; color:#FFF; border-radius:6px; padding:3px 10px; font-size:0.75rem;">Sign in</button></div></div>', unsafe_allow_html=True)
            if idx + 1 < len(integrations_data):
                with ic2:
                    t, d, ico = integrations_data[idx+1]
                    st.markdown(f'<div class="import-card"><div><span style="font-size:1.4rem;">{ico}</span><div style="font-weight:700; color:#FFF; margin-top:6px;">{t}</div><div style="font-size:0.76rem; color:#8B949E; margin-bottom:8px;">{d}</div><button style="background:#1E2636; border:1px solid #2B3547; color:#FFF; border-radius:6px; padding:3px 10px; font-size:0.75rem;">Sign in</button></div></div>', unsafe_allow_html=True)
            if idx + 2 < len(integrations_data):
                with ic3:
                    t, d, ico = integrations_data[idx+2]
                    st.markdown(f'<div class="import-card"><div><span style="font-size:1.4rem;">{ico}</span><div style="font-weight:700; color:#FFF; margin-top:6px;">{t}</div><div style="font-size:0.76rem; color:#8B949E; margin-bottom:8px;">{d}</div><button style="background:#1E2636; border:1px solid #2B3547; color:#FFF; border-radius:6px; padding:3px 10px; font-size:0.75rem;">Sign in</button></div></div>', unsafe_allow_html=True)

    with tab_custom:
        st.markdown(
            """
            <div style="background:#141822; border:1px solid #232B3A; border-radius:12px; padding:1.4rem; margin-top:1rem;">
                <h4 style="color:#FFF; margin:0 0 6px 0;">Agent remembers what matters to you</h4>
                <p style="color:#8B949E; font-size:0.86rem; margin-bottom:1.5rem;">As you work, Agent saves a short summary of your preferences and uses it across all projects and chats.</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem;">
                    <div>
                        <strong style="color:#FFF; font-size:0.9rem;">Memory</strong>
                        <div style="font-size:0.78rem; color:#8B949E;">Control whether Agent remembers your preferences in this workspace.</div>
                    </div>
                    <input type="checkbox" checked style="transform:scale(1.3);" />
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.4rem;">
                    <div>
                        <strong style="color:#FFF; font-size:0.9rem;">Memory in shared projects</strong>
                        <div style="font-size:0.78rem; color:#8B949E;">Control whether Agent uses your preferences in collaborative projects.</div>
                    </div>
                    <input type="checkbox" style="transform:scale(1.3);" />
                </div>
                <label style="font-size:0.84rem; font-weight:600; color:#CBD5E1;">What Agent remembers</label>
                <textarea style="width:100%; height:120px; background:#0E1117; border:1px solid #262E3E; border-radius:8px; color:#FFF; padding:10px; font-size:0.88rem; outline:none; margin-top:6px;" placeholder="Write what Agent should remember about you..."></textarea>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# SECTION 7: SECURITY (/security)
# ---------------------------------------------------------
elif st.session_state.current_nav == "Security":
    st.markdown('<h1 style="font-size:2rem; font-weight:700; color:#FFF; margin-bottom:0.4rem;">🛡️ Security Center</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8B949E; font-size:0.9rem; margin-bottom:1.5rem;">Automated vulnerability testing, secrets protection, and static code analysis.</p>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="import-card" style="margin-bottom:1.2rem;">
            <div>
                <strong style="color:#FFF; font-size:1rem;">Run a deep security scan</strong>
                <p style="color:#8B949E; font-size:0.84rem; margin:4px 0 10px 0;">Security Agent combines LLMs with leading static analysis tools to deliver a pen-test-grade report.</p>
                <button style="background:#0070F3; color:#FFF; border:none; border-radius:6px; padding:6px 14px; font-weight:600; cursor:pointer;">Run scan with Agent</button>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# SECTION 8: 2-COLUMN BUILD WORKSPACE
# ---------------------------------------------------------
elif st.session_state.current_nav == "Workspace":
    top_c1, top_c2 = st.columns([7, 3])
    with top_c1:
        st.markdown("### 📁 Ciwi AI Assistant · Live Build")
    with top_c2:
        if st.button("← Back to Home"):
            st.session_state.current_nav = "Home"
            st.rerun()

    c_chat, c_prev = st.columns([1, 1], gap="medium")

    with c_chat:
        chat_box = st.container(height=540)
        with chat_box:
            for m in st.session_state.messages:
                role = "assistant" if m["role"] == "model" else "user"
                with st.chat_message(role):
                    st.markdown(m["text"])

        if follow := st.chat_input("Message Agent..."):
            st.session_state.messages.append({"role": "user", "text": follow})
            reply = query_gemini(follow, is_design=True)
            if "```html" in reply:
                st.session_state.html_code = reply.split("```html")[1].split("```")[0].strip()
                st.session_state.messages.append({"role": "model", "text": reply.split("```html")[0].strip()})
            else:
                st.session_state.messages.append({"role": "model", "text": reply})
            st.rerun()

    with c_prev:
        components.html(st.session_state.html_code, height=580, scrolling=True)
