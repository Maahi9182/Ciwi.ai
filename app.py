import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Ciwi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS Styling ---
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
        max-width: 860px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 5rem !important;
        margin: 0 auto !important;
    }

    /* Top Navigation bar */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #111827;
    }

    .logo-icon {
        color: #F26522;
        font-size: 1.7rem;
    }

    /* Hero Text */
    .hero-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #111827;
        line-height: 1.05;
        margin-bottom: 0.6rem;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #6B7280;
        margin-bottom: 2.4rem;
    }

    /* Unified Search Capsule */
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

    [data-testid="stForm"] [data-testid="InputInstructions"],
    [data-testid="stForm"] div:has(> [data-testid="InputInstructions"]) {
        display: none !important;
    }

    [data-testid="stForm"] input {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 1.1rem !important;
        color: #111827 !important;
        padding: 0.6rem 0 !important;
    }

    /* Orange circular submit button */
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
        transition: transform 0.15s ease, background-color 0.15s ease;
        margin: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
        background-color: #DC5416 !important;
        transform: scale(1.05);
    }

    /* Secondary Pill buttons */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 12px !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
    }

    div.stButton > button:hover {
        border-color: #CBD5E1 !important;
        background-color: #F8FAFB !important;
    }

    .prompt-label {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.85rem;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
    }

    /* Auth card overlay */
    .auth-modal {
        background: #FFFFFF;
        border: 1px solid #E5E0D8;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }

    /* Response card */
    .response-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E0D8;
        border-radius: 18px;
        padding: 2rem;
        margin-top: 2.5rem;
        box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Check Streamlit Native OAuth Auth or Session State ---
# Streamlit has built-in st.experimental_user / st.user in modern versions
current_user = getattr(st, "user", None)
if current_user and getattr(current_user, "is_logged_in", False):
    st.session_state.authenticated = True
    st.session_state.user_name = current_user.name or current_user.email
    st.session_state.user_email = current_user.email

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "show_auth_modal" not in st.session_state:
    st.session_state.show_auth_modal = False
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Website"
if "query_value" not in st.session_state:
    st.session_state.query_value = ""

# --- Navigation Header ---
nav_left, nav_space, nav_auth = st.columns([5, 1.5, 2.5])

with nav_left:
    st.markdown(
        """
        <div class="logo-container">
            <span class="logo-icon">⠕</span> Ciwi
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
        c_profile, c_out = st.columns([2, 1.2])
        with c_profile:
            st.markdown(f"👤 **{st.session_state.user_name.split()[0]}**")
        with c_out:
            if st.button("Sign Out", use_container_width=True):
                if hasattr(st, "logout"):
                    try:
                        st.logout()
                    except Exception:
                        pass
                st.session_state.authenticated = False
                st.session_state.user_name = None
                st.session_state.user_email = None
                st.rerun()

# --- Auth Modal Dialog / Expander ---
if st.session_state.show_auth_modal and not st.session_state.authenticated:
    with st.container():
        st.markdown(
            """
            <div style="text-align:center; margin-bottom: 1rem;">
                <h3 style="margin:0; font-weight:700;">Welcome to Ciwi AI</h3>
                <p style="color:#6B7280; font-size:0.95rem; margin-top:4px;">Sign in or create your account to begin building</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_g, col_gh = st.columns(2)
        with col_g:
            if st.button("🔴 Continue with Google", use_container_width=True):
                if hasattr(st, "login"):
                    try:
                        st.login("google")
                    except Exception:
                        pass
                # Fallback prompt for quick demo or direct auth
                st.session_state.auth_provider = "Google"
        with col_gh:
            if st.button("🐙 Continue with GitHub", use_container_width=True):
                if hasattr(st, "login"):
                    try:
                        st.login("github")
                    except Exception:
                        pass
                st.session_state.auth_provider = "GitHub"

        st.markdown("<div style='text-align:center; color:#9CA3AF; margin: 0.8rem 0;'>— or use your email —</div>", unsafe_allow_html=True)

        auth_email = st.text_input("Email address", placeholder="you@example.com")
        auth_name = st.text_input("Your Full Name (optional for new account)", placeholder="John Doe")

        btn_c1, btn_c2 = st.columns([3, 1])
        with btn_c1:
            if st.button("Continue to Ciwi", use_container_width=True):
                if auth_email and "@" in auth_email:
                    st.session_state.authenticated = True
                    st.session_state.user_email = auth_email
                    st.session_state.user_name = auth_name if auth_name.strip() else auth_email.split("@")[0]
                    st.session_state.show_auth_modal = False
                    st.success(f"Welcome, {st.session_state.user_name}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
        with btn_c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_auth_modal = False
                st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #ECE7E1; margin: 2rem 0;'/>", unsafe_allow_html=True)

# --- Hero Title ---
st.markdown(
    """
    <div class="hero-title">What will you build?</div>
    <div class="hero-subtitle">Turn ideas into apps in minutes — no coding needed</div>
    """,
    unsafe_allow_html=True,
)

# --- Main Prompt Input Capsule ---
with st.form("prompt_form", clear_on_submit=False):
    c_input, c_btn = st.columns([15, 1])
    with c_input:
        prompt_input = st.text_input(
            "Prompt",
            value=st.session_state.query_value,
            placeholder=f"Build a {st.session_state.selected_mode.lower()} for...",
            label_visibility="collapsed",
        )
    with c_btn:
        submitted = st.form_submit_button("➔")

# --- Category Rack ---
cat1, cat2, cat3, cat4, cat5 = st.columns(5)
with cat1:
    if st.button("💻 Website", use_container_width=True):
        st.session_state.selected_mode = "Website"
with cat2:
    if st.button("🎨 Image Gen", use_container_width=True):
        st.session_state.selected_mode = "Image Gen"
with cat3:
    if st.button("📱 Mobile", use_container_width=True):
        st.session_state.selected_mode = "Mobile"
with cat4:
    if st.button("📐 Design", use_container_width=True):
        st.session_state.selected_mode = "Design"
with cat5:
    if st.button("🎞️ Animation", use_container_width=True):
        st.session_state.selected_mode = "Animation"

# --- Example Prompt Pills ---
st.markdown('<div class="prompt-label">Try an example prompt:</div>', unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    if st.button("Startup analytics dashboard", use_container_width=True):
        st.session_state.query_value = "Build a startup analytics dashboard"
        st.rerun()

with p2:
    if st.button("Cohort analysis dashboard", use_container_width=True):
        st.session_state.query_value = "Build a cohort analysis dashboard"
        st.rerun()

with p3:
    if st.button("Student budget tracker", use_container_width=True):
        st.session_state.query_value = "Build a student budget tracker"
        st.rerun()

# --- Response & Authentication Enforcement ---
if submitted and prompt_input:
    # Require Authentication Check:
    if not st.session_state.authenticated:
        st.session_state.show_auth_modal = True
        st.warning("⚠️ Please sign in or create an account with your Google, GitHub, or email to start building!")
        st.rerun()

    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        st.error("Missing GEMINI_API_KEY in Secrets.")
    else:
        client = genai.Client(api_key=api_key)
        st.markdown('<div class="response-card">', unsafe_allow_html=True)

        if st.session_state.selected_mode == "Image Gen":
            st.markdown(f"### 🎨 Visual Generator\n**Request:** *{prompt_input}*")
            with st.spinner("Generating art direction and visual blueprint..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"You are an elite creative director and visual designer. Provide a rich, "
                        f"cinematic image description, mood board colors, lighting details, and prompt for: {prompt_input}"
                    ),
                )
                st.markdown(response.text)
        else:
            with st.spinner(f"Ciwi is composing your {st.session_state.selected_mode}..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt_input,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            f"You are Ciwi, an elite AI builder helping user {st.session_state.user_name}. "
                            "Provide modular, production-ready code or architectures."
                        ),
                        temperature=0.7,
                    ),
                )
                st.markdown(response.text)

        st.markdown("</div>", unsafe_allow_html=True)
