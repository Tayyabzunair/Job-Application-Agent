import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq model — Llama 3.3 70B (powerful + free)
LLM_MODEL = "llama-3.3-70b-versatile"

# Paths
RESUME_JSON = "data/resume_data.json"
CHROMA_DIR = "chroma_db"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env file!")
# Add to src/config.py
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "job_agent_db"
COLLECTION_NAME = "applications"

if not MONGODB_URI:
    raise ValueError("MONGODB_URI missing in .env file!")
