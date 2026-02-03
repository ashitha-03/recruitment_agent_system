import streamlit as st

def load_styles():
    st.markdown("""
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 100%);
        font-family: "Inter", sans-serif;
    }

    /* Main card */
    .card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        padding: 28px;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.06);
        margin-bottom: 24px;
    }

    /* Titles */
    h1, h2, h3 {
        font-weight: 700;
        color: #1f2937;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 10px 26px !important;
        font-weight: 600 !important;
        transition: transform 0.1s ease;
    }

    .stButton>button:hover {
        transform: scale(1.02);
    }

    /* Text area & inputs */
    textarea, input {
        border-radius: 14px !important;
        background-color: #f9fafb !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f3f4f6 100%);
        border-right: 1px solid #e5e7eb;
    }

    </style>
    """, unsafe_allow_html=True)

def card_start():
    st.markdown('<div class="card">', unsafe_allow_html=True)

def card_end():
    st.markdown('</div>', unsafe_allow_html=True)
