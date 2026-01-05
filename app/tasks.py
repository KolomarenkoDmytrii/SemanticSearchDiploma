# https://jarrettmeyer.com/software/fastapi-celery/
# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#first-steps

import pathlib

import celery
import fastapi
import chromadb

from . import config
from . import models
from .dependencies import chroma_collections
from .docs_processing import docs_saving

celery_app = celery.Celery("tasks", broker=config.REDIS_URL, backend=config.REDIS_URL)


@celery_app.task(name="process_uploaded_doc")
def process_uploaded_doc(
    # filepath: str, docs_collection: chromadb.Collection
    filepath: str
):
    # contents = file.file.read()
    # filename = unicodedata.normalize("NFC", file.filename)
    filepath = pathlib.Path(filepath)

    with open(filepath, "rb") as f:
        # f.write(contents)
        contents = f.read()

    # try:
    #     # collection.add(
    #     #     documents=[contents.decode("utf-8")], ids=[file.filename]
    #     # )
    #     docs_processing.saving.save_doc_to_db(contents.decode("utf-8"), file.filename, collection)
    # except Exception:
    #     raise fastapi.HTTPException(
    #         status_code=500, detail="Error occured during processing the uploaded file"
    #     )

    # docs_saving.save_doc_to_db(contents.decode("utf-8"), file.filename, docs_collection)

    # docs_collection = chroma_collections.get_docs_collection(chroma_collections.get_chroma_client())
    # docs_saving.save_doc_to_db(contents, filepath.name, docs_collection)
    chroma_client = chroma_collections.get_chroma_client()
    docs_saving.save_doc_to_db(contents, filepath.name, chroma_client)

    return {"message": f"File '{filepath.name}' was successfuly uploaded"}


def get_task(task_id: str) -> models.TaskResponse:
    """
    Get detailed status of a specific task by ID.

    Uses Celery's AsyncResult which queries the Redis backend.
    This works for tasks in ANY state (pending, running, completed).

    Args:
        task_id: Unique task identifier

    Returns:
        TaskResponse with current task state and metadata
    """
    result = celery.result.AsyncResult(task_id, app=celery_app)

    return models.TaskResponse(
        task_id=task_id,
        state=result.state,
        name=result.name,
    )
