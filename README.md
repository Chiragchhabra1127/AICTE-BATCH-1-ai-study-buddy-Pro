📚 AI Study Buddy Pro

AI Study Buddy Pro is an AI-powered learning assistant built with Python, Streamlit, and Google Gemini AI. It helps students generate notes, explanations, summaries, flashcards, quizzes, and full mock exam papers — wrapped in a polished, themeable interface with voice input support.

---

🚀 Features

📝 Smart Notes
Generate clean, well-organized study notes on any topic, with headings, bullet points, bold key terms, and a summary section.

📖 Explain Topic
Get a clear explanation of any concept at your chosen level (Simple / Intermediate / Advanced), including a definition, key points, a real-world example, and a simple analogy.

📄 Summarize Text
Paste long notes or articles and get a one-line main idea, key bullet points, and important terms to remember.

🗂️ Flashcards
Auto-generate flip-style Q&A flashcards from any topic or pasted notes. Cards are parsed and displayed as individual cards with a "Reveal answer" expander — great for quick revision.

❓ Quiz Generator
Generate multiple-choice questions with adjustable difficulty and question count. Questions and options are auto-formatted so they always appear on clean, separate lines, with a full answer key at the end. Runs on a lighter, faster model for quicker results.

🎓 Exam Test Mode
Generate a complete, structured mock exam paper (Section A/B/C, marks per question, customizable total marks/duration/level) plus a model answer key — downloadable as a .txt file.

🎤 Ask a Doubt (Voice Enabled)
Type any question and get a clear, structured answer — or tap the microphone button to speak your question using your browser's built-in speech recognition (Chrome/Edge recommended), then copy the transcribed text into the question box.

🎨 Light / Dark Theme Toggle
Switch instantly between a warm cream "Light" theme and a deep navy "Dark" theme from the sidebar — both with a custom coral/amber accent palette and Fraunces + Inter typography.

---

🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini AI (google-genai SDK)
- python-dotenv
- Browser Web Speech API (for voice input)

---

📂 Project Structure

AI-Study-Buddy-Pro/
│
├── app.py
├── requirements.txt
├── README.md

---

🔑 Configure Gemini API Key

Option A — using a .env file (recommended for local use):
Create a ".env" file in the project root directory:

GEMINI_API_KEY=YOUR_API_KEY_HERE

Option B — enter it directly in the sidebar when the app is running. This is the easiest option, especially when deploying on Streamlit Cloud.

Get a free API key at: https://aistudio.google.com/apikey

---

▶️ Run the Application

streamlit run app.py

Open your browser and visit:
https://aicte-batch-1-ai-study-buddy-pro-4iehn5qma52xztmwnbqjdq.streamlit.app/

---

☁️ Deploying on Streamlit Cloud

1. Push app.py and requirements.txt to a GitHub repository.
2. Go to share.streamlit.io and connect your GitHub account.
3. Select the repository and app.py as the entry point, then deploy.
4. Once live, open the app and paste your Gemini API key into the sidebar to connect.
5. Any future updates pushed to the GitHub repo will automatically redeploy the app.

---

🎯 How to Use

1. Start the application (locally or via Streamlit Cloud).
2. Enter your Gemini API key in the sidebar (if not already set via .env).
3. Optionally switch between Light/Dark theme from the sidebar.
4. Pick a tab: Smart Notes, Explain, Summarize, Flashcards, Quiz, Exam Test, or Ask Doubt.
5. Enter a topic, paste text, or use the microphone (in Ask Doubt) to speak your question.
6. Click the relevant Generate button and view the AI-generated result instantly.
7. Exam papers can be downloaded as a .txt file directly from the app.

---

📸 Sample Topics

- Machine Learning
- Operating Systems
- Computer Networks
- Database Management System
- World History
- Photosynthesis / Newton's Laws

---

⚠️ Notes on API Usage

The free tier of the Gemini API has daily and per-minute request limits. If you see a "429 RESOURCE_EXHAUSTED" error, you have hit the free quota for the day — wait for it to reset or use a different API key. A "503 UNAVAILABLE" error means Google's servers are temporarily overloaded — simply retry after a short wait.

---

🔮 Future Enhancements

- PDF Upload & Analysis
- Download Notes/Flashcards as PDF
- Native in-app voice transcription (without manual copy-paste)
- Multi-language support
- Spaced-repetition flashcard scheduling
- User accounts with saved history

---

👨‍💻 Author

Chirag Chhabra

Built and iteratively upgraded as part of an AI internship project — AI Study Buddy Pro.

---

📄 License

This project is developed for educational and learning purposes.
