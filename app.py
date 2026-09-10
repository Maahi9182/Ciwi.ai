import os
import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="Ciwi AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Design styling
st.markdown(
    """
    <style>
    /* Warm canvas & typography */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    .block-container {
        max-width: 820px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
    }

    /* Top Navigation */
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.5rem;
        font-weight: 800;
        color: #111827;
        letter-spacing: -0.03em;
    }

    .brand-icon {
        color: #F26522;
        font-size: 1.6rem;
    }

    /* Hero Text */
    .hero-title {
        text-align: center;
        font-size: 3.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #141414;
        margin-top: 2rem;
        margin-bottom: 0.4rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #6B7280;
        margin-bottom: 2.2rem;
    }

    /* Clean white inputs */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 16px !important;
        height: 3.4rem !important;
        font-size: 1.05rem !important;
        padding-left: 1.2rem !important;
        color: #111827 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03) !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #F26522 !important;
        box-shadow: 0 0 0 3px rgba(242, 101, 34, 0.12) !important;
    }

    /* Neutral secondary pill buttons */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #374151 !important;
        border: 1px solid #E5E0D8 !important;
        border-radius: 12px !important;
        padding: 0.45rem 0.9rem !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease-in-out;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }

    div.stButton > button:hover {
        border-color: #D1D5DB !important;
        background-color: #F9FAFB !important;
        color: #111827 !important;
    }

    /* Orange circular action button */
    .submit-btn div.stButton > button {
        background-color: #F26522 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        height: 3.4rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(242, 101, 34, 0.3) !important;
    }

    .submit-btn div.stButton > button:hover {
        background-color: #DC5416 !important;
        color: #FFFFFF !important;
    }

    /* Center prompt suggestions */
    .prompt-label {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.88rem;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
    }

    /* Result container card */
    .response-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E0D8;
        border-radius: 16px;
        padding: 1.8rem;
        margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
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
if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "Website"
if "prefill_query" not in st.session_state:
    st.session_state.prefill_query = ""

# Navigation Bar
nav_col1, nav_col2, nav_col3 = st.columns([4, 1, 1])

with nav_col1:
    st.markdown(
        """
        <div class="brand-wrap">
            <span class="brand-icon">⠕</span> Ciwi
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col2:
    if not st.session_state.authenticated:
        if st.button("Sign In", use_container_width=True):
            st.session_state.show_login = True
    else:
        st.write(f"👋 **{st.session_state.user_name}**")

with nav_col3:
    if not st.session_state.authenticated:
        if st.button("Create Account", use_container_width=True):
            st.session_state.show_login = True
    else:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

# Google Login Modal Dropdown
if st.session_state.get("show_login") and not st.session_state.authenticated:
    with st.expander("Sign in to ciwi.ai with google.com", expanded=True):
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            if st.button("Mahi Ch (mahich9182@gmail.com)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahi Ch"
                st.session_state.show_login = False
                st.rerun()
        with m_col2:
            if st.button("Mahesh (22b91a0134@gmail.com)", use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.user_name = "Mahesh"
                st.session_state.show_login = False
                st.rerun()

# Hero Header
st.markdown(
    """
    <div class="hero-title">What will you build?</div>
    <div class="hero-subtitle">Turn ideas into apps in minutes — no coding needed</div>
    """,
    unsafe_allow_html=True,
)

# Main Input Row
input_box_col, btn_box_col = st.columns([6, 1])

placeholder_text = {
    "Website": "Build a website for...",
    "Image Gen": "Describe the visual scene to generate...",
    "Mobile": "Build a mobile app for...",
    "Design": "Design an interface layout for...",
    "Animation": "Create an interactive animation for...",
}.get(st.session_state.selected_mode, "Build a website for...")

with input_box_col:
    query = st.text_input(
        label="Prompt",
        value=st.session_state.prefill_query,
        placeholder=placeholder_text,
        label_visibility="collapsed",
    )

with btn_box_col:
    st.markdown('<div class="submit-btn">', unsafe_allow_html=True)
    trigger_submit = st.button("➔", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Category Cards Below Input
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("💻  Website", use_container_width=True):
        st.session_state.selected_mode = "Website"
        st.rerun()
with c2:
    if st.button("🎨  Image Gen", use_container_width=True):
        st.session_state.selected_mode = "Image Gen"
        st.rerun()
with c3:
    if st.button("📱  Mobile", use_container_width=True):
        st.session_state.selected_mode = "Mobile"
        st.rerun()
with c4:
    if st.button("📐  Design", use_container_width=True):
        st.session_state.selected_mode = "Design"
        st.rerun()
with c5:
    if st.button("🎞️  Animation", use_container_width=True):
        st.session_state.selected_mode = "Animation"
        st.rerun()

# Example Prompt Pills
st.markdown('<div class="prompt-label">Try an example prompt:</div>', unsafe_allow_html=True)
ex_col1, ex_col2, ex_col3 = st.columns(3)

with ex_col1:
    if st.button("Startup analytics dashboard", use_container_width=True):
        st.session_state.prefill_query = "Build a startup analytics dashboard"
        st.rerun()

with ex_col2:
    if st.button("Cohort analysis dashboard", use_container_width=True):
        st.session_state.prefill_query = "Build a cohort analysis dashboard"
        st.rerun()

with ex_col3:
    if st.button("Student budget tracker", use_container_width=True):
        st.session_state.prefill_query = "Build a student budget tracker"
        st.rerun()

# Processing & Response Generation
if (trigger_submit or query) and trigger_submit:
    api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
    if not api_key:
        st.error("API Key missing. Please set GEMINI_API_KEY in Streamlit Secrets.")
    else:
        client = genai.Client(api_key=api_key)
        st.markdown('<div class="response-card">', unsafe_allow_html=True)

        if st.session_state.selected_mode == "Image Gen":
            st.markdown(f"**🎨 Generating Creative Visual Blueprint:** *{query}*")
            with st.spinner("Formulating artistic concept..."):
                resp = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=(
                        f"Act as an art director. Provide an image prompt, exact camera/lens settings, "
                        f"color palette, and cinematic lighting for: {query}"
                    ),
                )
                st.markdown(resp.text)
        else:
            with st.spinner(f"Ciwi is composing your {st.session_state.selected_mode} solution..."):
                resp = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=query,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "You are Ciwi, an elite AI builder. Provide concise, clean, "
                            "and directly applicable software code or structural plans."
                        ),
                        temperature=0.7,
                    ),
                )
                st.markdown(resp.text)

        st.markdown("</div>", unsafe_allow_html=True)
