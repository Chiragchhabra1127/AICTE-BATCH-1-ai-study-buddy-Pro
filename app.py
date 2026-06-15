import streamlit as st
import google.generativeai as genai

# 1. UI/UX Configuration (Modern Look)
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")

# Custom CSS for better UX
st.markdown("""
    <style>
    .stTextInput>div>div>input {border-radius: 10px;}
    .stTextArea>div>div>textarea {border-radius: 10px;}
    .stButton>button {border-radius: 10px; font-weight: bold; width: 100%;}
    </style>
""", unsafe_allow_html=True)

# 2. Session State Management (For Login)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# 3. Sidebar - Login Area
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3048/3048122.png", width=100)
    st.title("🔐 Login to Study Buddy")
    
    email_input = st.text_input("Enter Email ID", placeholder="student@example.com")
    api_key_input = st.text_input("Enter Gemini API Key", type="password", placeholder="AIzaSy...")
    
    if st.button("Secure Login"):
        if email_input and api_key_input:
            try:
                # API Key configure karna
                genai.configure(api_key=api_key_input)
                # Test the API key with a dummy call
                model = genai.GenerativeModel('gemini-1.5-flash')
                st.session_state.logged_in = True
                st.session_state.user_email = email_input
                st.success("Login Successful! 🎉")
                st.rerun()
            except Exception as e:
                st.error("Invalid API Key! Please try again.")
        else:
            st.warning("Please enter both Email and API Key.")
            
    st.markdown("---")
    st.markdown("**Note:** Get your free API key from [Google AI Studio](https://aistudio.google.com/).")

# 4. Main Application Area (Only visible after login)
if st.session_state.logged_in:
    st.title("📚 AI-Powered Study Buddy")
    st.markdown(f"Welcome back, **{st.session_state.user_email}**! What do you want to learn today?")
    
    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Tabs for different student needs
    tab1, tab2, tab3 = st.tabs(["🧠 Explain Concept", "📝 Summarize Notes", "❓ Generate Quiz"])
    
    # --- TAB 1: Explain Concept ---
    with tab1:
        st.subheader("Understand Complex Topics Simply")
        concept = st.text_input("Enter a topic you are struggling with:", placeholder="e.g., Quantum Computing, Photosynthesis, Newton's Laws")
        
        if st.button("Explain to me like I'm 10"):
            if concept:
                with st.spinner("Thinking..."):
                    prompt = f"Explain the concept of '{concept}' in very simple, easy-to-understand terms. Use real-life examples. Structure it with bullet points."
                    response = model.generate_content(prompt)
                    st.info(response.text)
            else:
                st.error("Please enter a topic first.")

    # --- TAB 2: Summarize Notes ---
    with tab2:
        st.subheader("Summarize Long Study Notes")
        notes = st.text_area("Paste your long notes or lecture text here:", height=200)
        
        if st.button("Generate Summary"):
            if notes:
                with st.spinner("Condensing information..."):
                    prompt = f"Summarize the following study notes clearly and concisely. Highlight the key takeaways:\n\n{notes}"
                    response = model.generate_content(prompt)
                    st.success(response.text)
            else:
                st.error("Please paste some notes to summarize.")

    # --- TAB 3: Generate Quizzes ---
    with tab3:
        st.subheader("Test Your Knowledge")
        quiz_topic = st.text_input("Enter topic for a quick quiz:", placeholder="e.g., World War 2, Python Basics")
        difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])
        
        if st.button("Create Flashcards / Quiz"):
            if quiz_topic:
                with st.spinner("Generating questions..."):
                    prompt = f"Create a 5-question multiple-choice quiz on '{quiz_topic}' with '{difficulty}' difficulty. Provide the correct answers at the very end."
                    response = model.generate_content(prompt)
                    st.write(response.text)
            else:
                st.error("Please enter a topic to generate a quiz.")
else:
    st.info("👈 Please login from the sidebar using your Email and API Key to access the Study Buddy.")
