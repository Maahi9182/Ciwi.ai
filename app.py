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

st.markdown(
    """
    <style>
    /* Base background & typography */
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
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 3.5rem;
    }

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

    /* Outer Capsule Wrapper */
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

    /* Strip ALL internal Streamlit input borders & highlights */
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

    /* Remove the 'Press Enter to submit form' caption helper */
    [data-testid="stForm"] [data-testid="InputInstructions"],
    [data-testid="stForm"] div:has(> [data-testid="InputInstructions"]) {
        display: none !important;
    }

    /* Text input styling */
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

    /* Pill buttons for tabs and examples */
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

    /* Output Card */
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

# Session state setup
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Website"
if "query_value" not in st.session_state:
    st.session_state.query_value = ""

# --- Navigation Bar ---
nav_left, nav_space, nav_sign_in, nav_sign_up = st.columns([5, 2.5, 1.2, 1.5])

with nav_left:
    st.markdown(
        """
        <div class="logo-container">
            <span class="logo-icon">⠕</span> Ciwi
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_sign_in:
    if not st.session_state.authenticated:
        if st.button("Sign In", use_container_width=True):
            st.session_state.show_login = True
    else:
        st.write(f"**{st.session_state.user_name}**")

with nav_sign_up:
    if not st.session_state.authenticated:
        if st.button("Create Account", use_container_width=True):
            st.session_state.show_login = True
    else:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_name = None
            st.rerun()

# --- Sign-In Modal Dropdown ---
if st.session_state.get("show_login") and not st.session_state.authenticated:
    with st.expander("Sign in to ciwi.ai with Google", expanded=True):
        m1, m2 = st.columns(2)
        with m1:
            if st.button("Mahi Ch (mahich9182@gmail.com)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahi Ch"
                st.session_state.show_login = False
                st.rerun()
        with m2:
            if st.button("Mahesh (22b91a0134@gmail.com)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahesh"
                st.session_state.show_login = False
                st.rerun()

# --- Hero Title ---
st.markdown(
    """
    <div class="hero-title">What will you build?</div>
    <div class="hero-subtitle">Turn ideas into apps in minutes — no coding needed</div>
    """,
    unsafe_allow_html=True,
)

# --- Unified Search Bar ---
with st.form("prompt_form", clear_on_submit=False):
    c_input, c_btn = st.columns([15, 1])
    with c_input:
        prompt_input = st.text_input(
            "Prompt",
            value=st.session_state.query_value,
            placeholder="Build a website for...",
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

# --- Response Handling ---
if submitted and prompt_input:
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        st.error("Missing GEMINI_API_KEY in Secrets.")
    else:
        client = genai.Client(api_key=api_key)
        st.markdown('<div class="response-card">', unsafe_allow_html=True)
        with st.spinner(f"Ciwi is composing your {st.session_state.selected_mode}..."):
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt_input,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Ciwi, an elite AI builder. Provide clean, modular, "
                        "and immediately actionable plans or code."
                    ),
                    temperature=0.7,
                ),
            )
            st.markdown(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
