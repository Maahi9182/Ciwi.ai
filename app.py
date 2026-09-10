import os
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Ciwi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom High-End Styling
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        display: none !important;
    }

    .main .block-container {
        max-width: 920px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 5rem !important;
        margin: 0 auto !important;
    }

    /* Brand Header */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #111827;
    }

    .brand-icon {
        color: #F26522;
        font-size: 1.65rem;
    }

    /* Hero Text */
    .hero-title {
        text-align: center;
        font-size: 3.6rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #111827;
        margin-top: 1.2rem;
        margin-bottom: 0.3rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #6B7280;
        margin-bottom: 1.8rem;
    }

    /* Clean Search Capsule */
    [data-testid="stForm"] {
        border: 1.5px solid #E5E0D8 !important;
        background-color: #FFFFFF !important;
        border-radius: 28px !important;
        padding: 0.4rem 0.6rem 0.4rem 1.4rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        display: flex !important;
        align-items: center !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stForm"]:focus-within {
        border-color: #F26522 !important;
        box-shadow: 0 4px 24px rgba(242, 101, 34, 0.15) !important;
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
        margin: 0 !important;
    }

    [data-testid="stForm"] [data-testid="InputInstructions"] {
        display: none !important;
    }

    [data-testid="stForm"] input {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 1.08rem !important;
        color: #111827 !important;
        padding: 0.6rem 0 !important;
    }

    /* Orange Circle Submit Button */
    [data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        background-color: #F26522 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 2px 8px rgba(242, 101, 34, 0.35) !important;
        margin: 0 !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background-color: #DC5416 !important;
        transform: scale(1.05);
    }

    /* Pill Buttons */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 12px !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.9rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }

    div.stButton > button:hover {
        border-color: #CBD5E1 !important;
        background-color: #F8FAFB !important;
    }

    /* Workspace / Preview Card */
    .preview-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E0D8;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1.8rem;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }

    .badge-bar {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 1rem;
    }

    .live-badge {
        background: #10B981;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# State initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Website"
if "query_value" not in st.session_state:
    st.session_state.query_value = ""
if "show_auth_modal" not in st.session_state:
    st.session_state.show_auth_modal = False
if "last_generated_code" not in st.session_state:
    st.session_state.last_generated_code = ""

# Handle incoming OAuth redirects if handled via parameters
params = st.query_params
if "code" in params and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_name = "Authenticated User"
    st.session_state.user_email = "verified@google.com"

# --- Navigation Bar ---
nav_left, nav_space, nav_auth = st.columns([5, 1.5, 2.5])

with nav_left:
    st.markdown(
        """
        <div class="brand-wrap">
            <span class="brand-icon">⠕</span> Ciwi
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_auth:
    if not st.session_state.authenticated:
        c_in, c_up = st.columns(2)
        with c_in:
            if st.button("Sign In", use_container_width=True):
                st.session_state.show_auth_modal = True
        with c_up:
            if st.button("Create Account", use_container_width=True):
                st.session_state.show_auth_modal = True
    else:
        c_user, c_logout = st.columns([2, 1])
        with c_user:
            st.markdown(f"👤 **{st.session_state.user_name}**")
        with c_logout:
            if st.button("Sign Out", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_name = None
                st.rerun()

# --- Auth Modal with Real SVG Logos ---
if st.session_state.show_auth_modal and not st.session_state.authenticated:
    with st.container():
        st.markdown(
            """
            <div style="background: #FFFFFF; border: 1px solid #E5E0D8; border-radius: 18px; padding: 1.8rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.06);">
                <div style="text-align:center; margin-bottom: 1.2rem;">
                    <h3 style="margin:0; font-weight:800; font-size: 1.5rem; color:#111827;">Sign in to Ciwi AI</h3>
                    <p style="color:#6B7280; font-size:0.95rem; margin-top:4px;">Deploy and generate apps in minutes</p>
                </div>
            """,
            unsafe_allow_html=True,
        )

        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            "client_id=7627406237-uq7ob5hblfeep6a7f1rk9b25ia0mr0a8.apps.googleusercontent.com&"
            "response_type=code&"
            "scope=openid%20email%20profile&"
            "redirect_uri=https://ciwi-ai.streamlit.app/oauth2callback"
        )

        auth_btn1, auth_btn2 = st.columns(2)
        with auth_btn1:
            st.markdown(
                f"""
                <a href="{google_auth_url}" target="_self" style="text-decoration:none;">
                    <div style="display:flex; align-items:center; justify-content:center; gap:10px; background:#FFFFFF; border:1px solid #E5E0D8; border-radius:12px; padding:0.6rem 1rem; color:#1F2937; font-weight:600; font-size:0.92rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                        <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
                        Google
                    </div>
                </a>
                """,
                unsafe_allow_html=True,
            )
        with auth_btn2:
            st.markdown(
                """
                <div style="display:flex; align-items:center; justify-content:center; gap:10px; background:#FFFFFF; border:1px solid #E5E0D8; border-radius:12px; padding:0.6rem 1rem; color:#1F2937; font-weight:600; font-size:0.92rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03); cursor:pointer;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#111827"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                    GitHub
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='text-align:center; color:#9CA3AF; margin: 1rem 0 0.5rem 0;'>— or continue with email —</div>", unsafe_allow_html=True)
        acc_email = st.text_input("Email", placeholder="you@domain.com")
        c1, c2 = st.columns([3, 1])
        with c1:
            if st.button("Enter Ciwi", use_container_width=True):
                if acc_email and "@" in acc_email:
                    st.session_state.authenticated = True
                    st.session_state.user_name = acc_email.split("@")[0]
                    st.session_state.show_auth_modal = False
                    st.rerun()
        with c2:
            if st.button("Close", use_container_width=True):
                st.session_state.show_auth_modal = False
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# --- Hero Title ---
st.markdown(
    """
    <div class="hero-title">What will you build?</div>
    <div class="hero-subtitle">Turn ideas into apps in minutes — no coding needed</div>
    """,
    unsafe_allow_html=True,
)

# --- Search Bar Capsule ---
with st.form("main_form", clear_on_submit=False):
    col_inp, col_btn = st.columns([15, 1])
    with col_inp:
        user_input = st.text_input(
            "Prompt",
            value=st.session_state.query_value,
            placeholder=f"Build a {st.session_state.selected_mode.lower()} for...",
            label_visibility="collapsed",
        )
    with col_btn:
        exec_click = st.form_submit_button("➔")

# --- Category Selection with Active State ---
cat_names = [
    ("Website", "💻"),
    ("Image Gen", "🎨"),
    ("Mobile", "📱"),
    ("Design", "📐"),
    ("Animation", "🎞️"),
]
cat_cols = st.columns(len(cat_names))

for idx, (c_name, c_ico) in enumerate(cat_names):
    with cat_cols[idx]:
        is_selected = st.session_state.selected_mode == c_name
        label = f"{c_ico} {c_name}" + (" ●" if is_selected else "")
        if st.button(label, key=f"cat_{c_name}", use_container_width=True):
            st.session_state.selected_mode = c_name
            st.rerun()

# --- Example Prompt Pills ---
st.markdown("<div style='text-align:center; color:#9CA3AF; font-size:0.85rem; margin: 1.5rem 0 0.8rem 0;'>Try an example prompt:</div>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    if st.button("Startup analytics dashboard", use_container_width=True):
        st.session_state.query_value = "Build a startup analytics dashboard"
        st.rerun()

with p2:
    if st.button("Clothing brand showcase", use_container_width=True):
        st.session_state.query_value = "Build a vintage clothing brand storefront website"
        st.rerun()

with p3:
    if st.button("Student budget tracker", use_container_width=True):
        st.session_state.query_value = "Build an interactive student budget tracker web app"
        st.rerun()

# --- Execution, Workspace, Live Preview & Publish ---
if (exec_click and user_input) or st.session_state.last_generated_code:
    if not st.session_state.authenticated:
        st.session_state.show_auth_modal = True
        st.warning("⚠️ Please sign in or create an account to run and publish builds.")
        st.rerun()

    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

    if exec_click and user_input:
        if not api_key:
            st.error("Missing GEMINI_API_KEY in Secrets.")
        else:
            client = genai.Client(api_key=api_key)

            if st.session_state.selected_mode in ["Website", "Mobile", "Animation"]:
                with st.spinner("⚡ Ciwi is generating the complete standalone application..."):
                    gen_prompt = (
                        f"Build a production-grade, complete, self-contained single-page HTML/CSS/JS application for: {user_input}. "
                        "Return ONLY functional code wrapped in ```html ``` markdown blocks. "
                        "Include modern styling, clean UI layout, interactive JavaScript features, and responsive design."
                    )
                    resp = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=gen_prompt,
                    )
                    raw_text = resp.text
                    st.session_state.last_generated_code = raw_text

            else:
                with st.spinner(f"Ciwi is designing your {st.session_state.selected_mode}..."):
                    resp = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction="You are Ciwi, an elite AI builder. Provide concise, premium designs and specs.",
                            temperature=0.7,
                        ),
                    )
                    st.session_state.last_generated_code = resp.text

    # --- Live Preview & Publish Section ---
    if st.session_state.last_generated_code:
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)

        # Code Parsing for Embedded Live Previews
        code_content = st.session_state.last_generated_code
        html_code = ""
        if "```html" in code_content:
            html_code = code_content.split("```html")[1].split("```")[0].strip()
        elif "```" in code_content:
            html_code = code_content.split("```")[1].split("```")[0].strip()

        # Action Bar with Publish Button
        head_col, act_col1, act_col2 = st.columns([4, 1.3, 1.3])
        with head_col:
            st.markdown(
                """
                <div class="badge-bar">
                    <span class="live-badge">Live Workspace</span>
                    <strong style="font-size:1.1rem; color:#111827;">Interactive Application Preview</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with act_col1:
            if html_code:
                st.download_button(
                    "⬇️ Export HTML",
                    data=html_code,
                    file_name="ciwi_app.html",
                    mime="text/html",
                    use_container_width=True,
                )
        with act_col2:
            if st.button("🚀 Publish Live", use_container_width=True):
                st.balloons()
                st.success("App successfully deployed to your Ciwi live sandbox!")

        # Embedded Interactive Preview Window
        if html_code:
            tab_preview, tab_source = st.tabs(["🖥️ Live Interactive View", "📄 Code View"])
            with tab_preview:
                components.html(html_code, height=560, scrolling=True)
            with tab_source:
                st.code(html_code, language="html")
        else:
            st.markdown(code_content)

        st.markdown("</div>", unsafe_allow_html=True)
