from typing import Annotated

import fastapi

import chromadb
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

from .. import config


def get_chroma_client() -> chromadb.PersistentClient:
    chroma_client = chromadb.PersistentClient()
    return chroma_client


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
