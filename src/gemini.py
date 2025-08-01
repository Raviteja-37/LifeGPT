import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load the API key from the .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini SDK
genai.configure(api_key=GOOGLE_API_KEY)

# ✅ Corrected model name
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Generate a learning plan based on user input
def generate_learning_plan(prompt):
    try:
        # Stream the full content to avoid truncation
        response = model.generate_content(prompt, stream=True)

        # Collect all parts of the response
        full_text = ""
        for chunk in response:
            if hasattr(chunk, "text"):
                full_text += chunk.text

        return full_text or "❌ No response generated."

    except Exception as e:
        return f"❌ Error generating plan: {str(e)}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating plan: {str(e)}"
