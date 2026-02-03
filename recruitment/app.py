import streamlit as st
from db import init_db, save_history, get_history
from auth import login_block, logout_block
from ui import load_styles, card_start, card_end
from ai_logic import load_resumes, rank_candidates, ai_recommend

# ---- PAGE STATE PERSISTENCE ----
if "page" not in st.session_state:
    st.session_state.page = "Best Fit Recommendation"


init_db()
load_styles()
login_block()
logout_block()

resumes = load_resumes()

st.markdown("## 🎯 Recruiter Dashboard")
st.caption("AI-powered candidate recommendation system")


pages = ["Best Fit Recommendation", "Resume Explorer", "History"]

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page)
)

st.session_state.page = page


# -----------------------------
# BEST FIT PAGE
# -----------------------------
if page == "Best Fit Recommendation":
    

    card_start()

    st.markdown("### 📝 Job Requirements")

    job_desc = st.text_area(
        "",
        placeholder="e.g. Looking for a Machine Learning engineer with Python and SQL experience",
        height=120
    )

    st.markdown("#### 🔍 What the system does")
    st.markdown(
        "- 📄 Parses resumes\n"
        "- 🧠 Matches relevant skills\n"
        "- 🤖 Uses AI to explain best-fit candidate"
    )

    if st.button("✨ Find Best Fit"):
        if not job_desc.strip():
            st.warning("⚠️ Please enter job requirements to get recommendations.")
            st.stop()

        results = rank_candidates(job_desc, resumes)
        best = results[0]

        st.markdown("### 🏆 Recommended Candidate")
        st.success(f"**{best['candidate']}**")
        st.write("Matched skills:", ", ".join(best["matched"]) or "No exact match")

        save_history(
            st.session_state.username,
            job_desc,
            best["candidate"],
            ", ".join(best["matched"])
        )

        with st.expander("🤖 AI Recruiter Insight"):
            st.write(ai_recommend(job_desc, resumes))

    card_end()


# -----------------------------
# RESUME EXPLORER
# -----------------------------
elif page == "Resume Explorer":
    st.subheader("📄 Resume Explorer")

    names = [r["name"] for r in resumes]
    selected = st.selectbox("Select Candidate", names)

    resume = next(r for r in resumes if r["name"] == selected)

    st.markdown("**Resume Content:**")
    st.text_area("", resume["text"], height=300)

# -----------------------------
# HISTORY
# -----------------------------
elif page == "History":
    st.subheader("🕘 Recommendation History")

    rows = get_history(st.session_state.username)

    if not rows:
        st.info("No recommendations yet.")
    else:
        for jd, candidate, skills in rows:
            with st.container(border=True):
                st.markdown(f"**Job Description:** {jd[:100]}...")
                st.markdown(f"🏆 **Best Fit:** {candidate}")
                st.markdown(f"✅ **Matched Skills:** {skills or 'None'}")
