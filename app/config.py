import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "embeddinggemma")
DATA_DIRECTORY = pathlib.Path(os.getenv("DATA_DIRECTORY", "data"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-service:11434")

REDIS_URL = os.getenv(
    "REDIS_URL", "redis://redis-service:6379"
)  # https://stackoverflow.com/a/78262829

# DOC_CHUNK_SIZE = 640
# CHUNK_OVERLAP_RATIO = 0.25
DOC_CHUNK_SIZE = 512
CHUNK_OVERLAP_RATIO = 0.15

CHROMA_DB_HOST = os.getenv("CHROMA_DB_HOST", "chroma-db")
CHROMA_DB_PORT = int(os.getenv("CHROMA_DB_PORT", "8000"))
CHROMA_DB_COLLECTION_NAME = os.getenv("CHROMA_DB_COLLECTION_NAME", "docs")
