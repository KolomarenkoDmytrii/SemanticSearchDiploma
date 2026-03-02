"""Main module with API routes definitions."""

# https://techstrong.ai/articles/an-ai-powered-document-search-app-with-chroma/
# https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0
# https://docs.trychroma.com/integrations/embedding-models/ollama

import os
import mimetypes
from typing import cast

import urllib

import fastapi
import chromadb

from . import tasks
from . import models
from .dependencies import chroma_collections
from . import config
from .docs_processing import docs_saving

app = fastapi.FastAPI()


@app.get("/search", response_model=None)
def search_docs(
    query: str,
    n_results: int = 30,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
) -> chromadb.api.QueryResult:
    """Search over saved documents.

    Args:
        query (str): User search query string.
        n_results (int): Maximum number of search results.
        docs_collection (chromadb.Collection): ChromaDB documents collection.

    Returns:
        chromadb.api.QueryResult: The search query results.
    """
    return docs_collection.query(query_texts=[query], n_results=n_results)


@app.post("/files/upload")
def upload_doc(file: fastapi.UploadFile) -> models.TaskResponse:
    """Upload file for saving and processing.

    Args:
        file (fastapi.UploadFile): The uploaded file for processing.
        docs_collection (chromadb.Collection): ChromaDB documents collection.

    Returns:
        models.TaskResponse: Information about a task of uploaded document processing.
    """
    if not file.content_type in docs_saving.SUPPORTED_FORMATS:
        raise fastapi.HTTPException(status_code=400, detail="Not supported file type")

    contents = file.file.read()
    if file.filename is None:
        raise fastapi.HTTPException(
            status_code=500, detail="Uploaded file hasn't a name"
        )

    filepath = config.DATA_DIRECTORY / "docs" / file.filename
    # Ensure directory exists before opening file
    filepath.parent.mkdir(exist_ok=True)
    try:
        with open(filepath, "wb") as f:
            f.write(contents)
    except OSError as exc:
        raise fastapi.HTTPException(
            status_code=500, detail="Error occured during saving the uploaded file"
        ) from exc
    finally:
        file.file.close()

    result = tasks.celery_app.send_task(
        "process_uploaded_doc",
        kwargs={"filepath": str(filepath)},
    )

    return models.TaskResponse(
        task_id=result.id, state=result.state, name="process_uploaded_doc"
    )


@app.get("/tasks/{task_id}")
def get_task(task_id: str) -> models.TaskResponse:
    """Get status of a specified task.

    Args:
        task_id (str): A task ID returned by `upload_doc()` route.

    Returns:
        models.TaskResponse: Information about a task of uploaded document processing.
    """
    return tasks.get_task(task_id)


@app.get("/files/list")
def list_files(
    docs_limit: int = 2000,
    docs_offset: int = 0,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
) -> models.FilesListingResponse:
    """Get a list of the stored documents filenames.

    Args:
        docs_limit (int): Maximum number of documents used to get filenames
            as used by `Collection.get()` method `limit` parameter.
        docs_offset (int): Offset of retrieved documents used to get filenames
            as used by `Collection.get()` method `offset` parameter.
        docs_collection (chromadb.Collection): ChromaDB documents collection.

    Returns:
        models.FilesListingResponse: A list of the stored documents filenames.
    """
    metadatas = docs_collection.get(
        limit=docs_limit, offset=docs_offset, include=["metadatas"]
    )["metadatas"]
    filenames = (
        list(set(cast(str, metadata["filename"]) for metadata in metadatas))
        if metadatas
        else []
    )
    return models.FilesListingResponse(filenames=filenames)


@app.delete("/files/delete/{filename}")
def delete_file(
    filename: str,
    docs_collection: chromadb.Collection = fastapi.Depends(
        chroma_collections.get_docs_collection
    ),
) -> models.FileRemovedResponse:
    """Delete the specified stored document by its filename.

    Args:
        filename (str): A filename of the deleted document.
        docs_collection (chromadb.Collection): ChromaDB documents collection.

    Returns:
        models.FileRemovedResponse: An acknowledgment of the document deletion.
    """
    docs_collection.delete(where={"filename": filename})

    try:
        os.remove(config.DATA_DIRECTORY / "docs" / filename)
        return models.FileRemovedResponse(filename=filename, removed=True)
    except FileNotFoundError as exc:
        raise fastapi.HTTPException(status_code=404, detail="File not found") from exc


# https://davidmuraya.com/blog/fastapi-file-downloads/
@app.get("/files/download/{filename}")
async def download_file(filename: str) -> fastapi.responses.FileResponse:
    """
    Download a stored document by its filename.

    Args:
        filename (str): The filename of a stored document.

    Returns:
        fastapi.responses.FileResponse: A document file for downloading.
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

    # HTTP headers accept only ASCII characters
    # https://stackoverflow.com/questions/43365640/set-unicode-filename-in-flask-response-header
    quoted_filename = urllib.parse.quote(filename, safe="!#$&+-.^_`|~")

    # return a FileResponse to stream the file
    return fastapi.responses.FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quoted_filename}",
            "Content-Encoding": "identity",  # Disable gzip compression
            "Content-Length": str(file_size),
        },
    )
