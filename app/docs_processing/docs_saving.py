import semchunk
import textxtract
import chromadb

from .. import config

SUPPORTED_FORMATS = (
    "text/plain", # .txt
    "text/markdown", # .md (Markdown)
    "application/rtf", # .rtf
    "application/pdf", # .pdf
    "text/html", # .html (HTML)
    "application/msword", # .doc
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document", # .docx
)


def split_doc_into_chuncks(doc: str) -> list[str]:
    chuncker = semchunk.chunkerify(
        lambda text: len(text.split()), config.DOC_CHUNK_SIZE
    )
    return chuncker(doc, overlap=config.CHUNK_OVERLAP_RATIO)


def save_doc_to_db(doc: bytes, doc_filename: str, collection: chromadb.Collection):
    extractor = textxtract.SyncTextExtractor()
    text = extractor.extract(doc, doc_filename)
    chunks = split_doc_into_chuncks(text)

    collection.add(
        documents=chunks,
        ids=[f"{doc_filename}-{i}" for i in range(len(chunks))],
        metadatas=[{"filename": doc_filename} for _ in range(len(chunks))],
    )
