import os
from typing import cast

import pytest
from fastapi.testclient import TestClient
import chromadb

from app.main import app
from app.dependencies import chroma_collections
from app.tasks import celery_app, process_uploaded_doc
from app import config


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def eager_celery(monkeypatch) -> None:
    # Force Celery tasks to run synchronously during tests
    monkeypatch.setattr("app.tasks.celery_app.conf.task_always_eager", True)
    monkeypatch.setattr("app.tasks.celery_app.conf.task_eager_propagates", True)
    monkeypatch.setattr("app.tasks.celery_app.conf.task_store_eager_result", True)


# send_task() do not respects eager mode, so replace it with delay(), which does
@pytest.fixture(autouse=True)
def patch_celery_send_task(monkeypatch) -> None:
    def fake_send_task(name, args=None, kwargs=None, **options):
        if name == "process_uploaded_doc":
            return process_uploaded_doc.delay(*(args or ()), **(kwargs or {}))
        raise ValueError(f"Unexpected task name: {name}")

    monkeypatch.setattr(celery_app, "send_task", fake_send_task)


@pytest.fixture(autouse=True)
def remove_docs_after_test() -> None:
    yield

    client = chroma_collections.get_chroma_client()
    collection = chroma_collections.get_docs_collection(client)

    metadatas = collection.get(limit=2000, offset=0, include=["metadatas"])["metadatas"]
    filenames = (
        list(set(cast(str, metadata["filename"]) for metadata in metadatas))
        if metadatas
        else []
    )

    for filename in filenames:
        os.remove(config.DATA_DIRECTORY / "docs" / filename)

    ids = collection.get()["ids"]
    if len(ids) > 0:
        collection.delete(ids)
