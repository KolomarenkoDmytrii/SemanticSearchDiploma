"""Docs processing utilities."""

from typing import cast

import semchunk
import textxtract  # type: ignore[import-untyped]
import chromadb

from .. import config

SUPPORTED_FORMATS = (
    "text/plain",  # .txt
    "text/markdown",  # .md (Markdown)
    "application/rtf",  # .rtf
    "application/pdf",  # .pdf
    "text/html",  # .html (HTML)
    "application/msword",  # .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
)


def split_doc_into_chuncks(doc: str) -> list[str]:
    """Split read document file content into chunks using
        parameters specified in app.config module.

    Args:
        doc (str): Read document file content.

    Returns:
        list[str]: A list of the generated chunks.
    """
    chuncker = semchunk.chunkerify(
        lambda text: len(text.split()), config.DOC_CHUNK_SIZE
    )
    return cast(list[str], chuncker(doc, overlap=config.CHUNK_OVERLAP_RATIO))


def save_doc_to_db(
    doc: bytes, doc_filename: str, docs_collection: chromadb.Collection
) -> None:
    """Process an uploaded document and save it to the database collection.

    Args:
        docs (bytes): A readed stored document file.
        doc_filename (str): The name of a stored document file.
        docs_collection (chromadb.Collection): A ChromaDB collection to which store processed data.
    """
    extractor = textxtract.SyncTextExtractor()
    text = extractor.extract(doc, doc_filename)
    chunks = split_doc_into_chuncks(text)

    for i in range(0, len(chunks), config.BATCH_SIZE):
        start = i
        end = (
            i + config.BATCH_SIZE
            if i + config.BATCH_SIZE < len(chunks)
            else len(chunks)
        )
        print(f"{doc_filename}: BATCH ({start}-{end} / {len(chunks)})")
        docs_collection.add(
            documents=chunks[start:end],
            ids=[f"{doc_filename}-{k}" for k in range(start, end)],
            metadatas=[{"filename": doc_filename} for _ in range(start, end)],
        )
