"""Module with configuration parameters."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LLM_MODEL: str = os.getenv("LLM_MODEL", "embeddinggemma")
DATA_DIRECTORY: Path = Path(os.getenv("DATA_DIRECTORY", "data"))
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://ollama-service:11434")

REDIS_URL: str = os.getenv(
    "REDIS_URL", "redis://redis-service:6379"
)  # https://stackoverflow.com/a/78262829

# DOC_CHUNK_SIZE = 640
# CHUNK_OVERLAP_RATIO = 0.25
DOC_CHUNK_SIZE: int = 512
CHUNK_OVERLAP_RATIO: float = 0.15
BATCH_SIZE: int = 5

CHROMA_DB_HOST: str = os.getenv("CHROMA_DB_HOST", "chroma-db")
CHROMA_DB_PORT: int = int(os.getenv("CHROMA_DB_PORT", "8000"))
CHROMA_DB_COLLECTION_NAME: str = os.getenv("CHROMA_DB_COLLECTION_NAME", "docs")
