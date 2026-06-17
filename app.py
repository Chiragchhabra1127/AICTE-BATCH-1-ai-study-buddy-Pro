import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import re
import streamlit.components.v1 as components

# ── ENV ──────────────────────────────────────────────
load_dotenv()
ENV_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"
QUIZ_MODEL_NAME = "gemini-2.5-flash-lite"

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="AI Study Buddy Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ────────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = ENV_API_KEY
if "client" not in st.session_state:
    st.session_state.client = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# ── THEME TOKENS ─────────────────────────────────────
THEMES = {
    "dark": {
        "bg": "#11151C", "bg2": "#171C26", "surface": "#1C2230", "surface2": "#242B3B",
        "border": "#2E3647", "text": "#EDEFF4", "muted": "#8B93A7", "dim": "#565F73",
        "accent": "#FF8A5C", "accent2": "#FFB37A", "accent-text": "#1A1006",
        "ink": "#A8C9A1", "rose": "#FF6B7A", "shadow": "rgba(0,0,0,0.4)",
    },
    "light": {
        "bg": "#FAF6EE", "bg2": "#F3ECDD", "surface": "#FFFFFF", "surface2": "#FBF7EF",
        "border": "#E5DBC6", "text": "#2C2417", "muted": "#7A6F5C", "dim": "#B3A78E",
        "accent": "#D9622B", "accent2": "#B94F1F", "accent-text": "#FFFFFF",
        "ink": "#3F6B47", "rose": "#C03B45", "shadow": "rgba(60,45,20,0.12)",
    }
}
T = THEMES[st.session_state.theme]

# ── CSS ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

.stApp {{
    background: {T['bg']};
    background-image: radial-gradient(circle at 15% 0%, {T['bg2']} 0%, {T['bg']} 55%);
    color: {T['text']};
}}

[data-testid="stSidebar"] {{
    background-color: {T['surface']};
    border-right: 1px solid {T['border']};
}}
[data-testid="stSidebar"] * {{ color: {T['text']}; }}

h1, h2, h3 {{
    font-family: 'Fraunces', serif !important;
    color: {T['text']} !important;
    letter-spacing: -0.01em;
}}

.eyebrow {{
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {T['accent']};
    background: {T['accent']}1A;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 14px;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div,
.stNumberInput > div > div > input {{
    background-color: {T['surface2']} !important;
    color: {T['text']} !important;
    border: 1.5px solid {T['border']} !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {T['accent']} !important;
    box-shadow: 0 0 0 3px {T['accent']}26 !important;
}}

.stButton > button {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']});
    color: {T['accent-text']};
    border: none;
    border-radius: 12px;
    font-weight: 700;
    padding: 11px 24px;
    width: 100%;
    font-size: 0.95rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 2px 10px {T['shadow']};
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px {T['accent']}40;
}}
.stButton > button:active {{ transform: translateY(0px) scale(0.98); }}

.stTabs [data-baseweb="tab-list"] {{
    background-color: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    color: {T['muted']};
    border-radius: 10px;
    font-weight: 600;
    padding: 9px 16px;
    transition: all 0.2s ease;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {T['accent']}, {T['accent2']}) !important;
    color: {T['accent-text']} !important;
    box-shadow: 0 2px 12px {T['accent']}50;
}}

.stAlert {{ border-radius: 12px; border: none; }}

hr {{ border-color: {T['border']}; }}

.result-shell {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 18px;
    padding: 24px 26px;
    margin-top: 18px;
    box-shadow: 0 8px 30px {T['shadow']};
    animation: fadeUp 0.45s ease;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.fc-card {{
    background: {T['surface2']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
    transition: border-color 0.2s, box-shadow 0.2s;
}}
.fc-card:hover {{
    border-color: {T['accent']};
    box-shadow: 0 6px 20px {T['accent']}22;
}}
.fc-q {{ color: {T['accent']}; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; }}
.fc-a {{ color: {T['text']}; font-size: 0.9rem; line-height: 1.6; }}

.hero-card {{
    background: {T['surface']};
    border: 1px solid {T['border']};
    border-radius: 18px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.2s;
}}
.hero-card:hover {{ transform: translateY(-3px); }}
.hero-icon {{ font-size: 1.6rem; margin-bottom: 6px; }}
.hero-title {{ font-weight: 700; color: {T['text']}; font-size: 0.95rem; }}
.hero-sub {{ color: {T['muted']}; font-size: 0.8rem; margin-top: 2px; }}

.conn-badge {{
    display: flex; align-items: center; gap: 8px;
    background: {T['ink']}1A; color: {T['ink']};
    border: 1px solid {T['ink']}40;
    border-radius: 10px; padding: 8px 12px;
    font-size: 0.85rem; font-weight: 600;
}}
.dot {{ width: 8px; height: 8px; border-radius: 50%; background: {T['ink']}; }}

.glow-label {{
    display: inline-block;
    background: {T['accent']};
    color: {T['accent-text']};
    padding: 3px 11px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    box-shadow: 0 0 16px {T['accent']}70;
    animation: pulse 2.2s ease-in-out infinite;
}}
@keyframes pulse {{
    0%, 100% {{ box-shadow: 0 0 12px {T['accent']}50; }}
    50% {{ box-shadow: 0 0 22px {T['accent']}90; }}
}}

label, .stMarkdown p {{ color: {T['muted']}; }}
::placeholder {{ color: {T['dim']} !important; }}

.footer-note {{
    color: {T['dim']}; font-size: 0.78rem; text-align: center; margin-top: 30px;
}}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Study Buddy Pro")
    st.caption("Your AI-powered learning desk")
    st.markdown("---")

    st.markdown("**Appearance**")
    theme_choice = st.radio(
        " ", ["🌙 Dark", "☀️ Light"],
        index=0 if st.session_state.theme == "dark" else 1,
        horizontal=True, label_visibility="collapsed", key="theme_radio"
    )
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

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
        st.markdown('<div class="conn-badge"><span class="dot"></span>Connected to Gemini</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Enter your API key to begin")
        st.caption("Free key: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")

    st.markdown("---")
    st.markdown("**Tools**")
    st.markdown("📝 Smart Notes · 📖 Explain · 📄 Summarize\n\n🗂️ Flashcards · ❓ Quiz · 🎓 Exam Test · 🎤 Ask Doubt")

# ── HEADER ───────────────────────────────────────────
st.markdown('<span class="eyebrow">YOUR AI LEARNING DESK</span>', unsafe_allow_html=True)
st.markdown("# 📚 AI Study Buddy Pro")
st.write("Generate notes, explanations, summaries, flashcards, quizzes, and full exam tests — powered by Gemini AI")

if not st.session_state.client:
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("💡", "Explain", "Understand any topic clearly"),
        ("🗂️", "Flashcards", "Quick flip-card revision"),
        ("❓", "Quiz", "Test yourself instantly"),
        ("🎓", "Exam Test", "Full mock paper + answers"),
    ]
    for col, (icon, title, sub) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(f"""<div class="hero-card">
                <div class="hero-icon">{icon}</div>
                <div class="hero-title">{title}</div>
                <div class="hero-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

st.markdown("---")

client = st.session_state.client

def ask(prompt):
    if not client:
        return None
    try:
        resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return resp.text
    except Exception as e:
        return f"❌ Error: {e}"

def ask_fast(prompt):
    """Faster, lighter model — used for quizzes where speed matters more than depth."""
    if not client:
        return None
    try:
        resp = client.models.generate_content(model=QUIZ_MODEL_NAME, contents=prompt)
        return resp.text
    except Exception as e:
        return f"❌ Error: {e}"

def force_mcq_format(text):
    """Guarantee each question and each option (A/B/C/D) renders on its own line,
    regardless of how the model formatted its output."""
    if not text or text.startswith("❌"):
        return text
    # Ensure a newline before Q-numbers like "Q1." "Q2)" etc.
    text = re.sub(r'\s*(Q\d+[\.\)])', r'\n\n\1', text)
    # Ensure a newline before option markers A) B) C) D) when they appear inline
    text = re.sub(r'\s+(?=[A-D]\))', r'\n', text)
    # Ensure a newline before the answer key header
    text = re.sub(r'\s*(✅?\s*ANSWER KEY)', r'\n\n\1\n', text, flags=re.IGNORECASE)
    # Ensure each "Q#: X" answer line in the key starts on its own line
    text = re.sub(r'\s*(Q\d+\s*:\s*[A-D])', r'\n\1', text)
    # Collapse 3+ blank lines down to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def require_client():
    if not client:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar first.")
        return False
    return True

def render_result(text):
    st.markdown(
        f'<div class="result-shell">',
        unsafe_allow_html=True
    )
    st.markdown(text)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📝 Smart Notes", "📖 Explain", "📄 Summarize",
    "🗂️ Flashcards", "❓ Quiz", "🎓 Exam Test", "🎤 Ask Doubt"
])

# ── TAB 1: NOTES ─────────────────────────────────────
with tab1:
    st.markdown('<span class="glow-label">STUDY NOTES</span>', unsafe_allow_html=True)
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
Format with clear section headings, bullet points, bold key terms, and a 'Key Terms' summary at the end."""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                render_result(result)

# ── TAB 2: EXPLAIN ───────────────────────────────────
with tab2:
    st.markdown('<span class="glow-label">EXPLANATION</span>', unsafe_allow_html=True)
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
Include a clear definition, 3-4 key points, one real-world example, and a simple analogy."""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                render_result(result)

# ── TAB 3: SUMMARIZE ─────────────────────────────────
with tab3:
    st.markdown('<span class="glow-label">SUMMARY</span>', unsafe_allow_html=True)
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
                prompt = f"""Summarize the following text clearly for a student.
Provide a one-line main idea, 5-7 key bullet points, and important terms to remember.

Text:
{text_in}"""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                render_result(result)

# ── TAB 4: FLASHCARDS ────────────────────────────────
with tab4:
    st.markdown('<span class="glow-label">FLASHCARDS</span>', unsafe_allow_html=True)
    st.subheader("🗂️ Flashcard Generator")
    st.caption("Turn any topic or notes into Q&A flashcards for quick revision")
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
Respond ONLY in this exact format:
Q: <question>
A: <answer>
(repeat for all {fc_count} cards, nothing else)"""
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
                                st.markdown(f"""<div class="fc-card">
                                    <div class="fc-q">🃏 Card {i+1}</div>
                                    <div class="fc-q" style="font-size:0.88rem">{q.strip()}</div>
                                </div>""", unsafe_allow_html=True)
                                with st.expander("Reveal answer"):
                                    st.markdown(f"**Answer:** {a.strip()}")
                    else:
                        st.success("Generated Successfully ✅")
                        render_result(result)

# ── TAB 5: QUIZ ──────────────────────────────────────
with tab5:
    st.markdown('<span class="glow-label">SELF-ASSESSMENT</span>', unsafe_allow_html=True)
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

Format EXACTLY like this, with each part on its own line (use actual line breaks, never put options in one paragraph):

**Q1. [Question text]**
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Q2. [Question text]**
A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

(continue this exact pattern for all {n_q} questions, with a blank line between each question)

At the very end, add:
✅ **ANSWER KEY**
Q1: [Letter]
Q2: [Letter]
(continue for all questions, each on its own line)"""
                result = ask_fast(prompt)
                result = force_mcq_format(result)
                st.success("Generated Successfully ✅")
                render_result(result)

# ── TAB 6: EXAM TEST MODE ────────────────────────────
with tab6:
    st.markdown('<span class="glow-label">FULL MOCK EXAM</span>', unsafe_allow_html=True)
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
                prompt = f"""Create a complete mock exam paper for: {exam_subject}
Level: {exam_level} | Total Marks: {exam_marks} | Duration: {exam_duration}

Structure:
- Header with subject, marks, duration, and instructions
- SECTION A (MCQ / very short answer, ~20% of marks)
- SECTION B (short answer, ~30% of marks)
- SECTION C (long answer, ~50% of marks)

IMPORTANT FORMATTING RULES:
- For any MCQ question, put each option (A, B, C, D) on its own separate line, never in one paragraph.
- Use markdown line breaks between every question and its options.
- Show marks per question in brackets, e.g. (5 marks).

End with:
✅ **MODEL ANSWER KEY** — brief correct points for every question, each on its own line."""
                result = ask(prompt)
                st.success("Exam Paper Generated ✅")
                render_result(result)
                st.download_button("⬇️ Download as Text File", data=result,
                    file_name=f"{exam_subject.replace(' ', '_')}_exam_paper.txt", mime="text/plain")

# ── TAB 7: ASK DOUBT (with voice input) ──────────────
with tab7:
    st.markdown('<span class="glow-label">NEW · VOICE ENABLED</span>', unsafe_allow_html=True)
    st.subheader("🎤 Ask Any Doubt")
    st.caption("Type your question, or tap the mic and speak it")

    accent_color = T['accent']
    surface_color = T['surface2']
    border_color = T['border']
    text_color = T['text']

    components.html(f"""
    <div style="font-family:'Inter',sans-serif;">
      <button id="mic-btn" style="
          background:{accent_color}; color:white; border:none; border-radius:12px;
          padding:12px 22px; font-weight:700; font-size:0.95rem; cursor:pointer;
          width:100%; transition:all 0.2s;">
          🎤 Tap to Speak Your Doubt
      </button>
      <div id="mic-status" style="margin-top:8px; font-size:0.8rem; color:{text_color}; opacity:0.7;"></div>
      <textarea id="voice-result" readonly style="
          width:100%; margin-top:10px; min-height:70px; padding:12px;
          background:{surface_color}; color:{text_color}; border:1.5px solid {border_color};
          border-radius:12px; font-family:'Inter',sans-serif; font-size:0.9rem; display:none;"></textarea>
      <button id="copy-btn" style="display:none; margin-top:8px; background:{surface_color}; color:{text_color};
          border:1.5px solid {border_color}; border-radius:10px; padding:8px 16px; cursor:pointer; width:100%;">
          📋 Copy text, then paste it below
      </button>
    </div>
    <script>
    const micBtn = document.getElementById('mic-btn');
    const status = document.getElementById('mic-status');
    const resultBox = document.getElementById('voice-result');
    const copyBtn = document.getElementById('copy-btn');
    let recognition;
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';
        micBtn.onclick = () => {{
            status.textContent = '🔴 Listening... speak now';
            recognition.start();
        }};
        recognition.onresult = (event) => {{
            const text = event.results[0][0].transcript;
            resultBox.style.display = 'block';
            resultBox.value = text;
            copyBtn.style.display = 'block';
            status.textContent = '✅ Got it! Copy the text below and paste into the question box.';
        }};
        recognition.onerror = (event) => {{
            status.textContent = '⚠️ Could not hear you. Please try again or type instead.';
        }};
        copyBtn.onclick = () => {{
            resultBox.select();
            document.execCommand('copy');
            copyBtn.textContent = '✅ Copied!';
            setTimeout(() => copyBtn.textContent = '📋 Copy text, then paste it below', 1500);
        }};
    }} else {{
        micBtn.disabled = true;
        micBtn.textContent = '🎤 Voice input not supported in this browser';
        status.textContent = 'Try Chrome or Edge on desktop, or type your question below.';
    }}
    </script>
    """, height=180)

    doubt = st.text_area("Your Question / Doubt", height=150,
        placeholder="e.g. What is the difference between speed and velocity? Why does ice float on water?", key="doubt_in")
    subject_doubt = st.text_input("Subject (optional)", placeholder="e.g. Physics, Maths, History", key="doubt_subj")
    if st.button("Get Answer 🤔", key="btn_doubt"):
        if not require_client():
            pass
        elif not doubt.strip():
            st.warning("Please type or paste your doubt.")
        else:
            with st.spinner("Finding your answer..."):
                prompt = f"""A student has this doubt{f' in {subject_doubt}' if subject_doubt else ''}: "{doubt}"
Answer clearly: direct answer in 2-3 sentences, detailed step-by-step explanation, a real-world example,
related concepts, and one memorable takeaway line."""
                result = ask(prompt)
                st.success("Generated Successfully ✅")
                render_result(result)

st.markdown('<p class="footer-note">Built with Streamlit + Google Gemini AI · AI Study Buddy Pro</p>', unsafe_allow_html=True)
