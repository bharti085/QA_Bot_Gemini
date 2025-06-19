import os
import google.generativeai as genai

# Set your Gemini API key here
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)

os.environ["GOOGLE_API_KEY"] = ""
