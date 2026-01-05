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


# def save_doc_to_db(doc: bytes, doc_filename: str, collection: chromadb.Collection):
def save_doc_to_db(doc: bytes, doc_filename: str, chroma_client: chromadb.Client):
    extractor = textxtract.SyncTextExtractor()
    text = extractor.extract(doc, doc_filename)
    chunks = split_doc_into_chuncks(text)

    # collection.add(
    #     documents=chunks,
    #     ids=[f"{doc_filename}-{i}" for i in range(len(chunks))],
    #     metadatas=[{"filename": doc_filename} for _ in range(len(chunks))],
    # )
    # for i, chunck in enumerate(chunks):
    #     collection.add(
    #         documents=chunck,
    #         ids=[f"{doc_filename}-{i}"],
    #         metadatas=[{"filename": doc_filename}],
    #     )

    docs_collection = chroma_collections.get_docs_collection(chroma_client)

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

    # ids = [f"{doc_filename}-{i}" for i in range(len(chunks))]
    # metadatas = [{"filename": doc_filename} for _ in range(len(chunks))]
    # batches = batch_utils.create_batches(
    #     api=chroma_client, ids=ids, documents=chunks, metadatas=metadatas
    # )
    # docs_collection = chroma_collections.get_docs_collection(chroma_client)
    # for batch in batches:
    #     print(
    #         f"----------Adding batch of size {len(batch[0])} (/ {len(batches)})----------"
    #     )
    #     # print(batch[0][0])
    #     # print(batch[1][0])
    #     # print(batch[2][0])
    #     # raise Exception()
    #     docs_collection.add(ids=batch[0], documents=batch[3], metadatas=batch[2])
