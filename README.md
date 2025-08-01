# 🎓 LifeGPT – Your Personal AI Learning Coach

LifeGPT is a smart and motivating learning assistant that generates **personalized, day-wise learning plans** using Google’s Gemini API and fetches YouTube videos to support your learning. It’s built with **Python + Streamlit**, and designed to be clean, elegant, and inspiring to use.

## 🚀 Features

- ✅ Custom learning plan for any topic or goal
- 🧠 Powered by Gemini 1.5 Flash (Google Generative AI)
- 📺 Auto-fetches YouTube videos (via Pipedream)
- 🎨 Beautiful Streamlit frontend with modern glassy UI
- 🔐 Secure API management with `.env` file

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Gemini 1.5 Flash (`google.generativeai`)
- **Integrations**: YouTube, Notion (via Pipedream)


## 🧰 Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/lifegpt.git
   cd lifegpt

2. Create virtual environment
  python3 -m venv .venv
  source .venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt


4. Setup .env
Create a .env file in the root with:
  GOOGLE_API_KEY=your_gemini_api_key
  YOUTUBE_PIPEDREAM_URL=your_pipedream_post_url

5. Run the app
   streamlit run lifegpt_app.py




LifeGPT will return a structured plan like:
  Day 1:
- Topic: Python Basics
- Resources: "Python Programming - Full Course for Beginners [YouTube]"
- Tasks: Install Python, learn about variables and data types...

Day 2:
- Topic: Lists, Tuples, Dictionaries
- Resources: "Python Lists and Dictionaries - Crash Course"
- Tasks: Practice basic operations, slicing, and loops
...


