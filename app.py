import streamlit as st
import google.generativeai as genai

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0D1117;
    color: #E6EDF3;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #1C2333 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 24px;
    width: 100%;
    font-size: 15px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #5254CC, #7C3AED);
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}

/* Tabs */
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

/* Info/Success/Warning boxes */
.stAlert {
    border-radius: 12px;
    border: none;
}

/* Result boxes */
div[data-testid="stMarkdownContainer"] p {
    color: #E6EDF3;
    line-height: 1.7;
}

/* Divider */
hr {
    border-color: #30363D;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #6366F1 !important;
}

/* Cards */
.result-box {
    background: #161B22;
    border: 1px solid #30363D;
    border-radius: 14px;
    padding: 20px;
    margin-top: 16px;
}

.section-header {
    color: #A5B4FC;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

h1, h2, h3 {
    color: #E6EDF3 !important;
}

label {
    color: #7D8590 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ────────────────────────────────────
for key in ["logged_in", "user_name", "api_key"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "logged_in" else False

# ── SIDEBAR LOGIN ────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 StudyBuddy AI")
    st.markdown("---")

    if not st.session_state.logged_in:
        st.markdown("### 🔐 Login")
        name = st.text_input("Your Name", placeholder="e.g. Chirag Sharma")
        api_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
        st.caption("Get free key → [aistudio.google.com](https://aistudio.google.com/apikey)")

        if st.button("Login →"):
            if name.strip() and api_key.strip():
                try:
                    genai.configure(api_key=api_key.strip())
                    model_test = genai.GenerativeModel("gemini-1.5-flash")
                    model_test.generate_content("hi")
                    st.session_state.logged_in = True
                    st.session_state.user_name = name.strip()
                    st.session_state.api_key = api_key.strip()
                    st.success("Login successful!")
                    st.rerun()
                except Exception as e:
                    st.error(f"API Key error: {str(e)[:80]}")
            else:
                st.warning("Please enter name and API key.")
    else:
        st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
        st.markdown("---")
        st.markdown("**Tools Available:**")
        st.markdown("💡 Explain Concept")
        st.markdown("📄 Summarize Notes")
        st.markdown("📝 Smart Notes")
        st.markdown("🗂️ Flashcards")
        st.markdown("❓ Practice Quiz")
        st.markdown("🎤 Exam Prep")
        st.markdown("🤔 Ask a Doubt")
        st.markdown("---")
        if st.button("Logout"):
            for key in ["logged_in", "user_name", "api_key"]:
                st.session_state[key] = "" if key != "logged_in" else False
            st.rerun()

# ── MAIN AREA ────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("# 📚 StudyBuddy AI")
    st.markdown("### Your personal AI-powered learning assistant")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 💡 Explain")
        st.markdown("Understand any topic in simple language")
    with col2:
        st.markdown("#### ❓ Quiz")
        st.markdown("Test yourself with auto-generated MCQs")
    with col3:
        st.markdown("#### 🗂️ Flashcards")
        st.markdown("Create flip cards for quick revision")
    st.info("👈 Login from the sidebar using your Gemini API key to get started.")
    st.stop()

# ── LOGGED IN — SETUP MODEL ──────────────────────────
genai.configure(api_key=st.session_state.api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask(prompt):
    try:
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── HEADER ───────────────────────────────────────────
st.markdown(f"# 📚 StudyBuddy AI")
st.markdown(f"Welcome back, **{st.session_state.user_name}**! What do you want to study today?")
st.markdown("---")

# ── TABS ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💡 Explain",
    "📄 Summarize",
    "📝 Smart Notes",
    "🗂️ Flashcards",
    "❓ Quiz",
    "🎤 Exam Prep",
    "🤔 Ask Doubt"
])

# ── TAB 1: EXPLAIN ───────────────────────────────────
with tab1:
    st.subheader("💡 Explain Any Topic Simply")
    st.caption("Type any concept and get a clear, student-friendly explanation")
    topic = st.text_input("Topic", placeholder="e.g. Photosynthesis, Newton's Laws, Ohm's Law, French Revolution...")
    level = st.selectbox("Explanation Level", ["Simple (Class 10)", "Intermediate (Class 12)", "Advanced (College)"])
    if st.button("Explain it ✨", key="exp"):
        if topic.strip():
            with st.spinner("Generating explanation..."):
                prompt = f"""Explain the topic '{topic}' for a student at {level} level.
Structure your response as:
📌 DEFINITION: One clear sentence
🔑 KEY CONCEPTS: 4-5 bullet points
🌍 REAL-WORLD EXAMPLE: A relatable everyday example
📊 WHY IT MATTERS: Why students need to know this
💬 IN SIMPLE WORDS: Explain like the student is 12 years old
📝 EXAM TIP: What to remember for exams"""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please enter a topic.")

# ── TAB 2: SUMMARIZE ─────────────────────────────────
with tab2:
    st.subheader("📄 Summarize Your Notes")
    st.caption("Paste long notes or chapter text — get a clean summary instantly")
    notes = st.text_area("Paste your notes here", height=250,
        placeholder="Paste lecture notes, chapter text, or any long content...")
    if st.button("Summarize 📄", key="sum"):
        if notes.strip():
            with st.spinner("Summarizing..."):
                prompt = f"""Summarize the following study notes for a student.
Structure your response as:
📊 STATS: Word count reduced to key points
📋 MAIN TOPIC: What this is about (1 sentence)
🔑 KEY POINTS: 6-8 most important bullet points
🏷️ IMPORTANT TERMS: List the key vocabulary words
⚡ TL;DR: One-line summary

Notes:
{notes}"""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please paste some notes.")

# ── TAB 3: SMART NOTES ───────────────────────────────
with tab3:
    st.subheader("📝 Generate Smart Study Notes")
    st.caption("Turn rough or messy content into clean, organized study notes")
    raw = st.text_area("Paste rough notes or lecture content", height=250,
        placeholder="Paste rough notes, lecture transcript, or any disorganized content...")
    if st.button("Generate Clean Notes 📝", key="notes"):
        if raw.strip():
            with st.spinner("Organizing your notes..."):
                prompt = f"""Convert the following rough content into clean, well-organized study notes for a student.
Format with:
- Clear headings (use ▶ symbol)
- Bullet points under each heading
- Bold important terms
- A 'Key Terms' section at the end
- A 'Quick Revision Tips' section

Content:
{raw}"""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please paste some content.")

# ── TAB 4: FLASHCARDS ────────────────────────────────
with tab4:
    st.subheader("🗂️ Generate Flashcards")
    st.caption("Auto-generate Q&A flashcards from any topic or notes")
    fc_input = st.text_area("Topic or paste notes", height=150,
        placeholder="e.g. 'The French Revolution' or paste your notes here...")
    fc_count = st.slider("Number of flashcards", 4, 10, 6)
    if st.button("Make Flashcards 🗂️", key="fc"):
        if fc_input.strip():
            with st.spinner("Creating flashcards..."):
                prompt = f"""Create {fc_count} high-quality flashcards based on: {fc_input}

Format each card EXACTLY like this:
---
🃏 CARD [number]
Q: [Clear question]
A: [Concise, accurate answer]
---

Make questions exam-relevant. Cover the most important concepts."""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please enter a topic or paste notes.")

# ── TAB 5: QUIZ ──────────────────────────────────────
with tab5:
    st.subheader("❓ Practice Quiz")
    st.caption("Test your knowledge with auto-generated MCQ questions")
    quiz_topic = st.text_input("Quiz Topic", placeholder="e.g. World War 2, Python Basics, Human Digestive System")
    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    with col2:
        q_count = st.selectbox("Number of Questions", [3, 5, 8, 10])
    if st.button("Generate Quiz ❓", key="quiz"):
        if quiz_topic.strip():
            with st.spinner("Generating quiz..."):
                prompt = f"""Create a {q_count}-question multiple choice quiz on '{quiz_topic}' at {difficulty} difficulty.

Format:
Q1. [Question]
A) [Option]
B) [Option]
C) [Option]
D) [Option]

[Repeat for all questions]

✅ ANSWER KEY:
Q1: [Letter] - [Brief explanation]
[Continue for all]

Make questions exam-realistic."""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please enter a quiz topic.")

# ── TAB 6: EXAM PREP ─────────────────────────────────
with tab6:
    st.subheader("🎤 Exam Presentation Prep")
    st.caption("Get structured talking points and key facts to present any topic confidently")
    exam_topic = st.text_input("Topic to Present", placeholder="e.g. Climate Change, AI in Healthcare, Indian Economy")
    col1, col2 = st.columns(2)
    with col1:
        exam_type = st.selectbox("Exam Type", ["Viva / Oral Exam", "Written Exam", "Presentation / Seminar", "Interview"])
    with col2:
        subject = st.text_input("Subject (optional)", placeholder="e.g. Biology, History, Computer Science")
    if st.button("Prepare Me 🎤", key="exam"):
        if exam_topic.strip():
            with st.spinner("Preparing your exam content..."):
                prompt = f"""Prepare a student for a {exam_type} on the topic '{exam_topic}' {f'in {subject}' if subject else ''}.

Provide:
🎯 TOPIC OVERVIEW: 2-3 line introduction to say/write
📌 5 KEY POINTS: Most important facts to remember
❓ LIKELY QUESTIONS: 5 questions the examiner might ask
✅ IDEAL ANSWERS: Short, crisp answers to each question
🔑 KEYWORDS TO USE: Technical terms that impress examiners
⚠️ COMMON MISTAKES: What students often get wrong
💡 CLOSING LINE: A strong sentence to end your answer/presentation"""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please enter a topic.")

# ── TAB 7: ASK DOUBT ─────────────────────────────────
with tab7:
    st.subheader("🤔 Ask Any Doubt")
    st.caption("Ask any question — get a clear, student-friendly answer instantly")
    doubt = st.text_area("Your Question / Doubt", height=150,
        placeholder="e.g. What is the difference between speed and velocity? Why does ice float on water? How does recursion work?")
    subject_doubt = st.text_input("Subject (optional)", placeholder="e.g. Physics, Maths, History")
    if st.button("Get Answer 🤔", key="doubt"):
        if doubt.strip():
            with st.spinner("Finding your answer..."):
                prompt = f"""A student has asked this doubt{f' in {subject_doubt}' if subject_doubt else ''}:

"{doubt}"

Answer clearly and helpfully:
✅ DIRECT ANSWER: Answer the question clearly in 2-3 sentences
📖 DETAILED EXPLANATION: Break it down step by step
🌍 EXAMPLE: Give a real-world or relatable example
🔗 RELATED CONCEPTS: What other topics connect to this
📝 REMEMBER THIS: One-line memory trick or key takeaway"""
                result = ask(prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("Please type your doubt.")
