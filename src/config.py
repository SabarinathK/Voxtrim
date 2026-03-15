import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv(dotenv_path=".env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
UPLOAD_DIR = "uploads"
FILLERS = ["um", "uh", "like", "you know"]
WORDS_PER_SUBTITLE = 5

os.makedirs(UPLOAD_DIR, exist_ok=True)

client = Groq(api_key=GROQ_API_KEY)

