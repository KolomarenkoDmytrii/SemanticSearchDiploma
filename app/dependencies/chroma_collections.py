from typing import Annotated

import fastapi

import chromadb
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

from .. import config

# # _chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_DB_PATH))

def get_chroma_client() -> chromadb.PersistentClient:
    # chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_DB_PATH))
    # return chroma_client
    chroma_client = chromadb.HttpClient(host=config.CHROMA_DB_HOST, port=config.CHROMA_DB_PORT)
    return chroma_client
    # # return _chroma_client


def get_docs_collection(
    chroma_client: Annotated[
        chromadb.PersistentClient, fastapi.Depends(get_chroma_client)
    ],
) -> chromadb.Collection:
    collection = chroma_client.get_or_create_collection(
        name=config.CHROMA_DB_COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(
            model_name=config.LLM_MODEL,
            url=config.OLLAMA_URL,
        ),
    )

    return collection
