import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "university_docs"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

GROQ_MODEL = "llama-3.1-8b-instant"
OPENROUTER_MODEL = "anthropic/claude-3.5-sonnet"
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4

DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
