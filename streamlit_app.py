import streamlit as st
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Interview Prep Coach", layout="wide")
st.title("Interview Prep Coach")

# --- Sidebar: Create Session ---
with st.sidebar:
    st.header("New Session")
    company = st.text_input("Company", placeholder="e.g. Google")
    role = st.text_input("Role", placeholder="e.g. Backend Engineer")
    stage = st.selectbox("Stage", ["screening", "hiring_manager", "technical", "system_design"])
    jd_text = st.text_area("Paste Job Description", height=200)

    if st.button("Create Session"):
        if company and role and jd_text:
            resp = requests.post(f"{API_BASE}/sessions/", json={
                "company": company,
                "role": role,
                "jd_text": jd_text,
                "stage": stage,
            })
            if resp.status_code == 200:
                session = resp.json()
                st.session_state["active_session"] = session
                st.session_state.pop("questions", None)
                st.session_state.pop("feedback_results", None)
                st.success(f"Session created: {session['id']}")
            else:
                st.error(f"Error: {resp.text}")
        else:
            st.warning("Fill in all fields.")

    st.divider()
    st.header("Load Existing Session")
    if st.button("Refresh Sessions"):
        resp = requests.get(f"{API_BASE}/sessions/")
        if resp.status_code == 200:
            st.session_state["all_sessions"] = resp.json()

    if "all_sessions" in st.session_state:
        for s in st.session_state["all_sessions"]:
            label = f"{s['company']} - {s['role']} ({s['id']})"
            if st.button(label, key=f"load_{s['id']}"):
                st.session_state["active_session"] = s
                st.session_state.pop("questions", None)
                st.session_state.pop("feedback_results", None)

# --- Main Area ---
session = st.session_state.get("active_session")

if session is None:
    st.info("Create or load a session from the sidebar to get started.")
    st.stop()

st.subheader(f"{session['company']} — {session['role']}")
st.caption(f"Session ID: {session['id']} | Stage: {session['stage']}")

if session.get("skills_extracted"):
    st.write("**Extracted Skills:**", ", ".join(session["skills_extracted"]))

# --- Generate Questions ---
st.divider()
st.subheader("Generate Questions")

col1, col2 = st.columns(2)
with col1:
    q_types = st.multiselect(
        "Question Types",
        ["behavioral", "technical", "system_design"],
        default=["behavioral", "technical", "system_design"],
    )
with col2:
    count = st.number_input("Questions per type", min_value=1, max_value=10, value=3)

if st.button("Generate"):
    resp = requests.post(f"{API_BASE}/questions/generate", json={
        "session_id": session["id"],
        "types": q_types,
        "count_per_type": count,
    })
    if resp.status_code == 200:
        st.session_state["questions"] = resp.json()
        st.session_state["feedback_results"] = {}
        st.success(f"Generated {len(resp.json())} questions!")
    else:
        st.error(f"Error: {resp.text}")

# Load existing questions if not yet loaded
if "questions" not in st.session_state:
    resp = requests.get(f"{API_BASE}/questions/{session['id']}")
    if resp.status_code == 200 and resp.json():
        st.session_state["questions"] = resp.json()
        st.session_state.setdefault("feedback_results", {})

# --- Practice Questions ---
questions = st.session_state.get("questions", [])
if not questions:
    st.stop()

st.divider()
st.subheader("Practice")

for i, q in enumerate(questions):
    with st.expander(f"Q{i+1} [{q['type']}]: {q['text'][:80]}...", expanded=(i == 0)):
        st.write(q["text"])
        if q.get("skill_tags"):
            st.caption(f"Skills: {', '.join(q['skill_tags'])} | Difficulty: {q.get('difficulty', 'medium')}")

        answer = st.text_area("Your Answer", key=f"answer_{q['id']}", height=150)

        if st.button("Get Feedback", key=f"fb_{q['id']}"):
            if answer.strip():
                resp = requests.post(f"{API_BASE}/feedback/evaluate", json={
                    "question_id": q["id"],
                    "session_id": session["id"],
                    "answer_text": answer,
                })
                if resp.status_code == 200:
                    st.session_state["feedback_results"][q["id"]] = resp.json()
                else:
                    st.error(f"Error: {resp.text}")
            else:
                st.warning("Write an answer first.")

        # Show feedback if available
        fb = st.session_state.get("feedback_results", {}).get(q["id"])
        if fb:
            st.divider()
            score_col1, score_col2 = st.columns([1, 3])
            with score_col1:
                st.metric("Overall", f"{fb['overall_score']}/5")
            with score_col2:
                st.write(f"**Suggestion:** {fb['suggestion']}")

            criteria_cols = st.columns(5)
            criteria_keys = [
                ("has_concrete_example", "Example"),
                ("has_metric", "Metrics"),
                ("is_concise", "Concise"),
                ("answers_the_question", "Relevant"),
                ("uses_star_format", "STAR"),
            ]
            for col, (key, label) in zip(criteria_cols, criteria_keys):
                with col:
                    c = fb[key]
                    st.metric(label, f"{c['score']}/5")
                    st.caption(c["comment"])
