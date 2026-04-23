from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# =========================
# Base paths
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge-base"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

# =========================
# Embedding configuration
# =========================
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-base-en-v1.5")

# =========================
# Ollama / LLM configuration
# =========================
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# =========================
# Retrieval configuration
# =========================
TOP_K = int(os.getenv("TOP_K", 8))

# =========================
# Chunking configuration
# =========================
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

# =========================
# Chroma collection name
# =========================
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

# =========================
# Utility checks
# =========================
def ensure_directories() -> None:
    """
    Ensure required directories exist.
    """
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("KNOWLEDGE_BASE_DIR:", KNOWLEDGE_BASE_DIR)
    print("VECTOR_DB_DIR:", VECTOR_DB_DIR)
    print("EMBEDDING_MODEL_NAME:", EMBEDDING_MODEL_NAME)
    print("OLLAMA_MODEL:", OLLAMA_MODEL)
    print("TOP_K:", TOP_K)
    print("CHUNK_SIZE:", CHUNK_SIZE)
    print("CHUNK_OVERLAP:", CHUNK_OVERLAP)
    print("COLLECTION_NAME:", COLLECTION_NAME)