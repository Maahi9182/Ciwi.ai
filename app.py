import os
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ciwi AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Replit-Style Warm Editorial Theme CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global Base */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        color: #1A1A1A !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    /* Top Navigation Bar */
    .replit-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 1rem 2rem 1rem;
        border-bottom: 1px solid #ECE7E1;
        margin-bottom: 2.5rem;
    }

    .nav-left {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    .brand-logo {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-size: 1.45rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.03em;
    }

    .brand-mark {
        color: #F26522;
        font-size: 1.5rem;
    }

    .nav-links {
        display: flex;
        gap: 1.5rem;
        font-size: 0.95rem;
        color: #4B5563;
        font-weight: 500;
    }

    /* Hero Center Section */
    .hero-container {
        text-align: center;
        max-width: 820px;
        margin: 0 auto 2rem auto;
    }

    .hero-title {
        font-size: 3.6rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        color: #1A1A1A;
        line-height: 1.15;
        margin-bottom: 0.8rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #6B7280;
        font-weight: 400;
        margin-bottom: 1.8rem;
    }

    /* Primary Prompt Box Styling */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 16px !important;
        padding: 1.2rem 1.4rem !important;
        font-size: 1.05rem !important;
        color: #111827 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease;
    }

    div[data-testid="stTextInput"] > div > div > input:focus {
        border-color: #F26522 !important;
        box-shadow: 0 4px 24px rgba(242, 101, 34, 0.15) !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        border: 1px solid #E5E0D8 !important;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #F26522 !important;
        color: #F26522 !important;
    }

    /* Orange Primary Accent Button */
    .primary-btn div.stButton > button {
        background-color: #F26522 !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    .primary-btn div.stButton > button:hover {
        background-color: #D95316 !important;
        color: #FFFFFF !important;
    }

    /* Result Card */
    .output-card {
        background: #FFFFFF;
        border: 1px solid #E5E0D8;
        border-radius: 16px;
        padding: 1.8rem;
        margin-top: 1.5rem;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.04);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# State Management
# ---------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "active_mode" not in st.session_state:
    st.session_state.active_mode = "Chat & Build"
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

# ---------------------------------------------------------
# Top Header / Nav
# ---------------------------------------------------------
col_nav_left, col_nav_right = st.columns([3, 1])

with col_nav_left:
    st.markdown(
        """
        <div class="brand-logo">
            <span class="brand-mark">⠕</span> Ciwi
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_nav_right:
    if not st.session_state.authenticated:
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Sign In"):
                st.session_state.show_auth = "signin"
        with btn_col2:
            if st.button("Create Account"):
                st.session_state.show_auth = "signup"
    else:
        u_col1, u_col2 = st.columns([2, 1])
        with u_col1:
            st.markdown(f"**{st.session_state.user_name}**")
        with u_col2:
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.rerun()

# ---------------------------------------------------------
# Sign In / Create Account Popover Modals
# ---------------------------------------------------------
if (
    st.session_state.get("show_auth")
    and not st.session_state.authenticated
):
    with st.expander(
        "🔐 Sign in to Ciwi with Google or Email",
        expanded=True,
    ):
        quick_col1, quick_col2 = st.columns(2)
        with quick_col1:
            if st.button("Continue as Mahi Ch (Google)"):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahi Ch"
                st.session_state.user_email = "mahich9182@gmail.com"
                st.session_state.show_auth = False
                st.rerun()
        with quick_col2:
            if st.button("Continue as Mahesh (Google)"):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahesh"
                st.session_state.user_email = "22b91a0134@gmail.com"
                st.session_state.show_auth = False
                st.rerun()

        st.divider()
        custom_email = st.text_input("Or enter custom email:")
        if st.button("Proceed"):
            if custom_email:
                st.session_state.authenticated = True
                st.session_state.user_name = custom_email.split("@")[0]
                st.session_state.user_email = custom_email
                st.session_state.show_auth = False
                st.rerun()

# ---------------------------------------------------------
# Hero Title Section
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">What will you build?</div>
        <div class="hero-subtitle">Turn ideas into apps, models, and images in seconds — no coding needed</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Category / Mode Tabs
# ---------------------------------------------------------
mode_cols = st.columns([1, 1, 1, 1, 1])

with mode_cols[0]:
    if st.button("💬 Chat & Build", use_container_width=True):
        st.session_state.active_mode = "Chat & Build"
with mode_cols[1]:
    if st.button("🎨 Image Generation", use_container_width=True):
        st.session_state.active_mode = "Image Generation"
with mode_cols[2]:
    if st.button("📱 Mobile", use_container_width=True):
        st.session_state.active_mode = "Mobile"
with mode_cols[3]:
    if st.button("📐 Design", use_container_width=True):
        st.session_state.active_mode = "Design"
with mode_cols[4]:
    if st.button("🎞 Animation", use_container_width=True):
        st.session_state.active_mode = "Animation"

# ---------------------------------------------------------
# Main Prompt Input Bar with Orange Submit Action
# ---------------------------------------------------------
placeholder_map = {
    "Chat & Build": "Build a website for...",
    "Image Generation": "Describe an image to generate (e.g. vintage retro aesthetic poster)...",
    "Mobile": "Build an iOS / Android experience for...",
    "Design": "Design a high-converting UI landing page for...",
    "Animation": "Create a smooth CSS/3D animation for...",
}

input_col, send_col = st.columns([5, 1])

with input_col:
    user_query = st.text_input(
        label="Prompt",
        placeholder=placeholder_map.get(
            st.session_state.active_mode, "Ask Ciwi anything..."
        ),
        label_visibility="collapsed",
    )

with send_col:
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    submit_clicked = st.button("Generate ➔", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Example Prompt Suggestion Pills
# ---------------------------------------------------------
st.caption("Try an example prompt:")
sug_col1, sug_col2, sug_col3 = st.columns(3)

with sug_col1:
    if st.button(
        "Startup analytics dashboard",
        key="s1",
        use_container_width=True,
    ):
        user_query = "Create a startup analytics dashboard"
        submit_clicked = True

with sug_col2:
    if st.button(
        "Vintage men's clothing store showcase",
        key="s2",
        use_container_width=True,
    ):
        user_query = "Design an online showcase for a vintage retro men's thrift brand"
        submit_clicked = True

with sug_col3:
    if st.button(
        "Student budget tracker",
        key="s3",
        use_container_width=True,
    ):
        user_query = "Build a student budget tracker app"
        submit_clicked = True

# ---------------------------------------------------------
# Processing & Output Generation
# ---------------------------------------------------------
if submit_clicked and user_query:
    api_key = st.secrets.get(
        "GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY")
    )
    if not api_key:
        st.error("Please add GEMINI_API_KEY to your Streamlit secrets.")
    else:
        client = genai.Client(api_key=api_key)

        st.markdown(
            '<div class="output-card">', unsafe_allow_html=True
        )

        if st.session_state.active_mode == "Image Generation":
            st.markdown(
                f"### 🎨 Image Generation Prompt\n**Prompt:** *{user_query}*"
            )
            with st.spinner(
                "Generating detailed cinematic creative concept & asset direction..."
            ):
                img_prompt_response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Act as a professional creative director and prompt engineer. "
                        f"Provide a photorealistic, stylized asset description, lighting setup, "
                        f"and photographic color palette for the user prompt: {user_query}"
                    ),
                )
                st.markdown(img_prompt_response.text)
        else:
            with st.spinner("Ciwi is composing your solution..."):
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=user_query,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are Ciwi, an elite, clean AI builder inspired by Replit. "
                            "Deliver concise, modular, and ready-to-use solutions with clear typography."
                        ),
                        temperature=0.7,
                    ),
                )
                st.markdown(response.text)

        st.markdown("</div>", unsafe_allow_html=True)
