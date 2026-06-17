import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re

# ── ENV ──────────────────────────────────────────────
load_dotenv()
ENV_API_KEY = os.getenv("GEMINI_API_KEY", "")

MODEL_NAME = "gemini-2.5-flash"

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS — Dark Pro UI ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

.stApp { background-color: #0D1117; color: #E6EDF3; }

[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}
[data-testid="stSidebar"] * { color: #E6EDF3; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background-color: #1C2333 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 10px !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 22px;
    width: 100%;
    font-size: 15px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5254CC, #7C3AED);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #161B22;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #7D8590;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background-color: #6366F1 !important;
    color: white !important;
}

.stAlert { border-radius: 12px; border: none; }

h1, h2, h3 { color: #E6EDF3 !important; }
label, .stMarkdown p { color: #C9D1D9; }

hr { border-color: #30363D; }

.fc-card {
    background: #1C2333;
    border: 1px solid #30363D;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.fc-q { color: #A5B4FC; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; }
.fc-a { color: #E6EDF3; font-size: 0.9rem; line-height: 1.6; }

.badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    color: #A5B4FC;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ENV_API_KEY
if "client" not in st.session_state:
    st.session_state.client = None

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Study Buddy Pro")
    st.caption("AI-powered learning assistant")
    st.markdown("---")

    key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Get a free key at aistudio.google.com/apikey"
    )

    if key_input != st.session_state.api_key:
        st.session_state.api_key = key_input
        st.session_state.client = None

    if st.session_state.api_key and st.session_state.client is None:
        try:
            st.session_state.client = genai.Client(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"Invalid key: {e}")

    if st.session_state.client:
        st.success("✅ Connected")
    else:
        st.warning("⚠️ Enter your API key to begin")
        st.caption("Free key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")

    st.markdown("---")
    st.markdown("**Tools**")
    st.markdown("📝 Smart Notes\n\n📖 Explain Topic\n\n📄 Summarize Text\n\n🗂️ Flashcards\n\n❓ Quiz Generator\n\n🎓 Exam Test Mode")

# ── HEADER ───────────────────────────────────────────
st.markdown("# 📚 AI Study Buddy Pro")
st.write("Generate notes, explanations, summaries, flashcards, quizzes, and full exam tests — powered by Gemini AI")
st.markdown("---")

client = st.session_state.client

def ask(prompt):
    """Send a prompt to Gemini and return text, or an error message."""
    if not client:
        return None
    try:
        resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return resp.text
    except Exception as e:
        return f"❌ Error: {e}"

def require_client():
    if not client:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar first.")
        return False
    return True

# ── TABS ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Smart Notes",
    "📖 Explain",
    "📄 Summarize",
    "🗂️ Flashcards",
    "❓ Quiz",
    "🎓 Exam Test"
])

# ── TAB 1: NOTES ─────────────────────────────────────
with tab1:
    st.markdown('<span class="badge">STUDY NOTES</span>', unsafe_allow_html=True)
    st.subheader("Generate Clean Study Notes")
    topic = st.text_area("Enter a topic", height=120,
        placeholder="e.g. Operating Systems, Machine Learning, Database Normalization...", key="notes_in")
    if st.button("Generate Notes 📝", key="btn_notes"):
        if not require_client():
            pass
        elif not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Creating your notes..."):
                prompt = f"""Create detailed, well-organized study notes on: {topic}

Format with:
- Clear section headings
- Bullet points under each heading
- Bold the most important terms
- A short 'Key Terms' summary at the end"""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                st.markdown(result)

# ── TAB 2: EXPLAIN ───────────────────────────────────
with tab2:
    st.markdown('<span class="badge">EXPLANATION</span>', unsafe_allow_html=True)
    st.subheader("Explain Any Topic Simply")
    topic2 = st.text_input("Enter a topic or concept", placeholder="e.g. Newton's Laws, Recursion, Photosynthesis...", key="explain_in")
    level = st.selectbox("Explanation Level", ["Simple (Beginner)", "Intermediate", "Advanced"], key="explain_lvl")
    if st.button("Explain it 📖", key="btn_explain"):
        if not require_client():
            pass
        elif not topic2.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Explaining..."):
                prompt = f"""Explain '{topic2}' in simple language at a {level} level for a student.
Include:
- A clear one-line definition
- 3-4 key points
- One real-world example
- A simple analogy"""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                st.markdown(result)

# ── TAB 3: SUMMARIZE ─────────────────────────────────
with tab3:
    st.markdown('<span class="badge">SUMMARY</span>', unsafe_allow_html=True)
    st.subheader("Summarize Long Text or Notes")
    text_in = st.text_area("Paste your text here", height=220,
        placeholder="Paste lecture notes, an article, or any long text...", key="sum_in")
    if st.button("Summarize 📄", key="btn_sum"):
        if not require_client():
            pass
        elif not text_in.strip():
            st.warning("Please paste some text.")
        else:
            with st.spinner("Summarizing..."):
                prompt = f"""Summarize the following text clearly and concisely for a student.
Provide:
- A one-line main idea
- 5-7 key bullet points
- The most important terms to remember

Text:
{text_in}"""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                st.markdown(result)

# ── TAB 4: FLASHCARDS ────────────────────────────────
with tab4:
    st.markdown('<span class="badge">NEW FEATURE</span>', unsafe_allow_html=True)
    st.subheader("🗂️ Flashcard Generator")
    st.caption("Turn any topic or notes into flip-style Q&A flashcards for quick revision")
    fc_input = st.text_area("Enter a topic or paste your notes", height=150,
        placeholder="e.g. 'Cell Biology' or paste a paragraph of notes...", key="fc_in")
    fc_count = st.slider("Number of flashcards", 4, 12, 6, key="fc_count")
    if st.button("Generate Flashcards 🗂️", key="btn_fc"):
        if not require_client():
            pass
        elif not fc_input.strip():
            st.warning("Please enter a topic or notes.")
        else:
            with st.spinner("Creating flashcards..."):
                prompt = f"""Create exactly {fc_count} flashcards based on: {fc_input}

Respond ONLY in this exact format, one card per pair of lines, nothing else:
Q: <question>
A: <answer>
Q: <question>
A: <answer>
(continue for all {fc_count} cards)"""
                result = ask(prompt)
                if result and result.startswith("❌"):
                    st.error(result)
                elif result:
                    pairs = re.findall(r"Q:\s*(.+?)\s*\n\s*A:\s*(.+?)(?=\nQ:|\Z)", result, re.DOTALL)
                    if pairs:
                        st.success(f"Generated {len(pairs)} flashcards ✅")
                        cols = st.columns(2)
                        for i, (q, a) in enumerate(pairs):
                            with cols[i % 2]:
                                with st.expander(f"🃏 Card {i+1}: {q.strip()[:60]}"):
                                    st.markdown(f"**Answer:** {a.strip()}")
                    else:
                        st.success("Generated Successfully ✅")
                        st.markdown(result)

# ── TAB 5: QUIZ ──────────────────────────────────────
with tab5:
    st.markdown('<span class="badge">SELF-ASSESSMENT</span>', unsafe_allow_html=True)
    st.subheader("Create a Practice Quiz")
    quiz_topic = st.text_input("Enter a topic for the quiz", placeholder="e.g. Computer Networks, World History...", key="quiz_in")
    col1, col2 = st.columns(2)
    with col1:
        n_q = st.number_input("Number of questions", min_value=3, max_value=20, value=10, key="quiz_n")
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"], key="quiz_diff")
    if st.button("Create Quiz ❓", key="btn_quiz"):
        if not require_client():
            pass
        elif not quiz_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating quiz..."):
                prompt = f"""Create {n_q} MCQ quiz questions with answers on: {quiz_topic}
Difficulty: {difficulty}

Format:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

Repeat for all questions, then add:
✅ ANSWER KEY
Q1: [Correct letter]
..."""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                st.markdown(result)

# ── TAB 6: EXAM TEST MODE ────────────────────────────
with tab6:
    st.markdown('<span class="badge">NEW FEATURE — FULL MOCK EXAM</span>', unsafe_allow_html=True)
    st.subheader("🎓 Exam Test Mode")
    st.caption("Generate a complete, structured mock exam paper for serious revision")

    exam_subject = st.text_input("Subject / Topic", placeholder="e.g. Database Management System, Operating Systems...", key="exam_subj")
    col1, col2, col3 = st.columns(3)
    with col1:
        exam_marks = st.selectbox("Total Marks", [25, 50, 75, 100], index=1, key="exam_marks")
    with col2:
        exam_duration = st.selectbox("Duration", ["30 mins", "1 hour", "2 hours", "3 hours"], index=1, key="exam_dur")
    with col3:
        exam_level = st.selectbox("Level", ["School", "College", "Competitive Exam"], key="exam_level")

    if st.button("Generate Exam Paper 🎓", key="btn_exam"):
        if not require_client():
            pass
        elif not exam_subject.strip():
            st.warning("Please enter a subject or topic.")
        else:
            with st.spinner("Preparing your exam paper..."):
                prompt = f"""Create a complete mock exam paper for the subject/topic: {exam_subject}
Level: {exam_level}
Total Marks: {exam_marks}
Duration: {exam_duration}

Structure the paper as:
📋 EXAM PAPER HEADER (subject, marks, duration, instructions)

SECTION A — Very Short Answer / MCQs (worth ~20% of marks)
SECTION B — Short Answer Questions (worth ~30% of marks)
SECTION C — Long Answer / Essay Questions (worth ~50% of marks)

For each question, mention the marks allotted in brackets, e.g. (5 marks).
At the very end, add:
✅ MODEL ANSWER KEY — brief correct answers/points for every question."""
                result = ask(prompt)
                st.success("Exam Paper Generated ✅")
                st.markdown(result)
                st.download_button(
                    "⬇️ Download as Text File",
                    data=result,
                    file_name=f"{exam_subject.replace(' ', '_')}_exam_paper.txt",
                    mime="text/plain"
                )

st.markdown("---")
st.caption("Built with Streamlit + Google Gemini AI · AI Study Buddy Pro")
