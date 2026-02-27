import itertools

import semchunk
import textxtract
import chromadb
from chromadb.utils import batch_utils

from .. import config
from ..dependencies import chroma_collections

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
    chuncker = semchunk.chunkerify(
        lambda text: len(text.split()), config.DOC_CHUNK_SIZE
    )
    return chuncker(doc, overlap=config.CHUNK_OVERLAP_RATIO)


def save_doc_to_db(doc: bytes, doc_filename: str, docs_collection: chromadb.Collection):
    extractor = textxtract.SyncTextExtractor()
    text = extractor.extract(doc, doc_filename)
    chunks = split_doc_into_chuncks(text)

    BATCH_SIZE = 5
    for i in range(0, len(chunks), BATCH_SIZE):
        start = i
        end = i + BATCH_SIZE if i + BATCH_SIZE < len(chunks) else len(chunks)
        print(
            f"--------------------BATCH ({start}-{end} / {len(chunks)})--------------------"
        )
        docs_collection.add(
            documents=chunks[start:end],
            ids=[f"{doc_filename}-{k}" for k in range(start, end)],
            metadatas=[{"filename": doc_filename} for _ in range(start, end)],
        )
