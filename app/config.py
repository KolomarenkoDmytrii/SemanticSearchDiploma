import pathlib

LLM_MODEL = "embeddinggemma"
DATA_DIRECTORY = pathlib.Path("data")
# Adjust the base URL as per your Ollama server configuration
OLLAMA_URL = "http://ollama:11434"
CHROMA_DB_COLLECTION_NAME = "docs"

REDIS_URL = "redis://redis:6379"  # https://stackoverflow.com/a/78262829

# DOC_CHUNK_SIZE = 640
# CHUNK_OVERLAP_RATIO = 0.25
DOC_CHUNK_SIZE = 512
CHUNK_OVERLAP_RATIO = 0.15

# CHROMA_DB_PATH = DATA_DIRECTORY / "chroma"
CHROMA_DB_HOST = "chroma-db"
CHROMA_DB_PORT = 8000
