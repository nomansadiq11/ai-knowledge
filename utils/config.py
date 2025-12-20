import os
from pathlib import Path

# Default to local Ollama; Docker compose can override via environment
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Default embedding model (can be overridden via env)
DEFAULT_EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-mpnet-base-v2"
)

# Uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
