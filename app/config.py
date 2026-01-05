import pathlib

LLM_MODEL = "embeddinggemma"
DATA_DIRECTORY = pathlib.Path("data")
# Adjust the base URL as per your Ollama server configuration
OLLAMA_URL = "http://ollama:11434"
CHROMA_DB_COLLECTION_NAME = "docs"

DOC_CHUNK_SIZE = 640
CHUNK_OVERLAP_RATIO = 0.25
