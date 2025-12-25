import semchunk
import chromadb

from .. import config


def split_doc_into_chuncks(doc: str) -> list[str]:
    chuncker = semchunk.chunkerify(lambda text: len(text.split()), config.DOC_CHUNK_SIZE)
    return chuncker(doc, overlap=config.CHUNK_OVERLAP_RATIO)


def save_doc_to_db(doc: str, doc_filename: str, collection: chromadb.Collection):
    chunks = split_doc_into_chuncks(doc)

    collection.add(
        documents=chunks,
        ids=[f"{doc_filename}-{i}" for i in range(len(chunks))],
        metadatas=[{"filename": doc_filename} for _ in range(len(chunks))],
    )
