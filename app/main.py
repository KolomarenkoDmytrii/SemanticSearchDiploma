# https://techstrong.ai/articles/an-ai-powered-document-search-app-with-chroma/
# https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0
# https://docs.trychroma.com/integrations/embedding-models/ollama

# TODO: Реалізувати вилучення документу
import os
import mimetypes

import fastapi
import chromadb

from .dependencies import chroma_collections
from . import config
from .docs_processing import docs_saving

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def search_docs(
    query: str,
    n_results: int = 30,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
):
    return docs_collection.query(query_texts=[query], n_results=n_results)


@app.post("/files/upload")
def upload_doc(
    file: fastapi.UploadFile,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
):
    if not file.content_type == "text/plain":
        raise fastapi.HTTPException(status_code=400, detail="Not supported file type")

    contents = file.file.read()

    try:
        with open(config.DATA_DIRECTORY / "docs" / file.filename, "wb") as f:
            f.write(contents)

    except Exception:
        raise fastapi.HTTPException(
            status_code=500, detail="Error occured during saving the uploaded file"
        )
    finally:
        file.file.close()

    # try:
    #     # collection.add(
    #     #     documents=[contents.decode("utf-8")], ids=[file.filename]
    #     # )
    #     docs_processing.saving.save_doc_to_db(contents.decode("utf-8"), file.filename, collection)
    # except Exception:
    #     raise fastapi.HTTPException(
    #         status_code=500, detail="Error occured during processing the uploaded file"
    #     )
    docs_saving.save_doc_to_db(contents.decode("utf-8"), file.filename, docs_collection)

    return {"message": f"File '{file.filename}' was successfuly uploaded"}


@app.get("/files/list")
def list_files(
    docs_limit: int = 100,
    docs_offset: int = 0,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
):
    filenames = list(
        set(
            metadata["filename"]
            for metadata in docs_collection.get(
                limit=docs_limit, offset=docs_offset, include=["metadatas"]
            )["metadatas"]
        )
    )
    return {"filenames": filenames}


@app.delete("/files/delete/{filename}")
def delete_file(
    filename: str,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
):
    docs_collection.delete(where={"filename": filename})

    try:
        os.remove(config.DATA_DIRECTORY / "docs" / filename)
        return {"filename": filename, "removed": True}
    except FileNotFoundError:
        # return fastapi.JSONResponse(
        #     content={
        #         "filename": filename,
        #         "removed": False,
        #         "error_message": "File not found",
        #     },
        #     status_code=404,
        # )
        raise fastapi.HTTPException(status_code=404, detail="File not found")


# https://davidmuraya.com/blog/fastapi-file-downloads/
@app.get("/files/download/{filename}")
async def download_file(filename: str):
    """
    Streams a file from the predefined static directory.
    """
    # Sanitize the filename to prevent directory traversal attacks.
    if ".." in filename or "/" in filename:
        raise fastapi.HTTPException(status_code=400, detail="Invalid filename")

    file_path = config.DATA_DIRECTORY / "docs" / filename

    if not file_path.exists():
        raise fastapi.HTTPException(status_code=404, detail="File not found")

    # Guess the media type based on the file extension.
    media_type, _ = mimetypes.guess_type(file_path)
    if media_type is None:
        media_type = "application/octet-stream"  # Default for unknown file types

    file_size = file_path.stat().st_size

    # Return a FileResponse to stream the file.
    return fastapi.responses.FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Encoding": "identity",  # Disable gzip compression
            "Content-Length": str(file_size),
        },
    )
