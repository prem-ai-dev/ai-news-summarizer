from google import genai
from app.core.config import access

api_key=access.GEMINI_API_KEY

client= genai.Client(api_key=api_key)