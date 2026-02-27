"""Chroma DB connection management."""

from typing import Annotated

import fastapi

import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

from .. import config


def get_chroma_client() -> chromadb.api.ClientAPI:
    """Get a ChromaDB client object using user connection parameters
        specified in the app.config module.

    Returns:
        chromadb.api.ClientAPI: A ChromaDB client connected
            to the database.
    """
    chroma_client = chromadb.HttpClient(
        host=config.CHROMA_DB_HOST, port=config.CHROMA_DB_PORT
    )
    return chroma_client


def get_docs_collection(
    chroma_client: Annotated[
        chromadb.api.ClientAPI, fastapi.Depends(get_chroma_client)
    ],
) -> chromadb.Collection:
    """Get a ChromaDB collection used for storing processed data
        about uploaded documents.

    Args:
        chroma_client (chromadb.api.ClientAPI): A ChromaDB client connected
            to the database.

    Returns:
        chromadb.Collection: A ChromaDB collection used for storing processed data
            about uploaded documents.
    """
    collection = chroma_client.get_or_create_collection(
        name=config.CHROMA_DB_COLLECTION_NAME,
        # using `type: ignore` because text-only embedding functions can't be used typesafely
        # reference: https://github.com/chroma-core/chroma/issues/5241
        embedding_function=OllamaEmbeddingFunction(  # type: ignore
            model_name=config.LLM_MODEL,
            url=config.OLLAMA_URL,
        ),
    )

    return collection
