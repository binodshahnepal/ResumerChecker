import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Please set it in the .env file.")

UPLOAD_DIR = "data/uploads"
REPORT_DIR = "data/reports"
CHROMA_DIR = "chroma_store"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

LLM_MODEL = "gemini-2.5-pro"
EMBEDDING_MODEL = "models/text-embedding-004"
TEMPERATURE = 0.3
