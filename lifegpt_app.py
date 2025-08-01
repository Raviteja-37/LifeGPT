import streamlit as st
import os
from dotenv import load_dotenv
from src.utils import run_agent_sync
from src.prompt import build_learning_prompt
from src.gemini import generate_learning_plan

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
youtube_pipedream_url = os.getenv("YOUTUBE_PIPEDREAM_URL")

# --- Custom Glassmorphism CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    .main {
        padding: 2rem;
    }

    h1 {
        text-align: center;
        font-size: 3em;
        color: #00f7ff;
        text-shadow: 0 0 10px #00f7ff;
    }

    .glass-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .youtube-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI Starts Here ---
st.markdown("<h1>✨ LifeGPT Learning Companion</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    user_goal = st.text_input("🎯 What do you want to learn?", placeholder="e.g., Learn DSA in 30 days")
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("🚀 Generate Learning Plan"):
    if not user_goal:
        st.warning("Please enter a learning goal.")
    elif not google_api_key:
        st.error("Missing Google API Key. Please check your .env file.")
    else:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.info("⏳ Generating your plan...")

        def show_progress(msg):
            st.write("📍", msg)

        result = run_agent_sync(
            google_api_key=google_api_key,
            youtube_pipedream_url=youtube_pipedream_url,
            user_goal=user_goal,
            progress_callback=show_progress,
        )

        st.success("✅ Learning Plan Ready!")
        st.subheader("📚 Your Plan:")

        for msg in result["messages"]:
            st.markdown(f"<div class='youtube-card'>{msg}</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
