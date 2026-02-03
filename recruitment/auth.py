import streamlit as st
import re
from db import create_user, authenticate_user

# ==============================
# CONFIG
# ==============================
ACCESS_CODE = "RECRUIT-2026"

# ==============================
# PASSWORD VALIDATION
# ==============================
def validate_password(password: str):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""

# ==============================
# LOGIN / REGISTER BLOCK
# ==============================
def login_block():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return

    # ---- CENTERED CARD LAYOUT ----
    left, center, right = st.columns([1, 1.4, 1])

    with center:
        st.markdown(
            """
            <div style="text-align:center; margin-bottom:15px;">
                <h1>🤖 Recruiter Portal</h1>
                <p>Secure access for recruiters</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        # ==============================
        # LOGIN TAB
        # ==============================
        with tab1:
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input(
                "Password", type="password", placeholder="Enter password"
            )

            if st.button("Login", use_container_width=True):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login successful")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

        # ==============================
        # REGISTER TAB
        # ==============================
        with tab2:
            new_username = st.text_input(
                "New Username", placeholder="Choose a username"
            )
            new_password = st.text_input(
                "New Password", type="password", placeholder="Choose a strong password"
            )
            access_code = st.text_input(
                "Access Code", type="password", placeholder="Company access code"
            )

            st.caption(
                "🔒 Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )

            if st.button("Register", use_container_width=True):
                if access_code != ACCESS_CODE:
                    st.error("❌ Wrong access code")
                else:
                    valid, msg = validate_password(new_password)
                    if not valid:
                        st.error(f"❌ {msg}")
                    elif create_user(new_username, new_password):
                        st.success("✅ Account created successfully. Please login.")
                    else:
                        st.error("❌ Username already exists")

    st.stop()

# ==============================
# LOGOUT
# ==============================
def logout_block():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.pop("username", None)
        st.rerun()
