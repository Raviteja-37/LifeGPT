print("👋 Hello from LifeGPT")

import os
from dotenv import load_dotenv
from src.utils import run_agent_sync
from src.prompt import build_learning_prompt
from src.gemini import generate_learning_plan
import google.generativeai as genai


# load additional pipedream URLs
youtube_pipedream_url = os.getenv("YOUTUBE_PIPEDREAM_URL")


print("📦 Loading .env file...")

# Load environment variables from .env
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
print("🔑 API Key:", "✅ Found" if google_api_key else "❌ Not Found")

if google_api_key:
    print("✅ Successfully loaded Google API Key")
else:
    print("❌ Failed to load API Key. Check your .env file.")
    exit()

def get_user_goal():
    print("\n📘 Tell me what you want to learn:")
    goal = input("👉 Your learning goal (e.g., 'Learn Python basics in 5 days'): ")
    return goal

if __name__ == "__main__":
    goal = get_user_goal()
    print(f"\n🎯 Learning Goal: {goal}")
    
    def progress(msg):
        print("📍", msg)

    result = run_agent_sync(
        google_api_key=google_api_key,
        youtube_pipedream_url=youtube_pipedream_url,
        user_goal=goal,
        progress_callback=progress
    )

