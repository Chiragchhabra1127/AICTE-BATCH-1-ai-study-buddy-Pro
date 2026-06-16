import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Config
st.set_page_config(
    page_title="AI Study Buddy Pro",
    page_icon="📘",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', sans-serif; }
    .main { background-color: #f9f9f9; }
    textarea { font-size: 16px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📘 AI Study Buddy")
st.write("Generate Notes, Summaries, Explanations and Quiz Questions using Gemini AI")

# Sidebar
st.sidebar.header("Options")
study_type = st.sidebar.selectbox(
    "Select Task",
    ["Generate Notes", "Explain Topic", "Create Quiz", "Summarize Text"]
)

dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
download_option = st.sidebar.checkbox("⬇️ Enable Download")

# User Input
user_input = st.text_area("Enter Topic or Text", height=200)

# Generate Button
if st.button("Generate Study Material"):
    if user_input.strip() == "":
        st.warning("Please enter a topic or text.")
    else:
        if study_type == "Generate Notes":
            prompt = f"Create detailed study notes on: {user_input}"
        elif study_type == "Explain Topic":
            prompt = f"Explain this topic in simple language: {user_input}"
        elif study_type == "Create Quiz":
            prompt = f"Create 10 MCQ quiz questions with answers on: {user_input}"
        elif study_type == "Summarize Text":
            prompt = f"Summarize the following text: {user_input}"

        try:
           with st.spinner("Generating..."):
               response = model.generate_content(prompt)

           if response and response.text:
               st.success("Generated Successfully ✅")
               st.write(response.text)
       else:
            st.error("No response received. Check API key or quota.")
except Exception as e:
    st.error(f"Error: {e}")
          
            # Download Option
            if download_option:
                st.download_button(
                    label="Download Output",
                    data=response.text,
                    file_name="study_material.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"Error: {e}")

# Dark Mode Toggle
if dark_mode:
    st.markdown(
        "<style>body { background-color: #1e1e1e; color: white; }</style>",
        unsafe_allow_html=True
    )
