import pytest
from fastapi.testclient import TestClient

print("IMPORTING APP")
from app.main import app

print("APP IMPORTED")
from app.dependencies import chroma_collections
from app.tasks import celery_app, process_uploaded_doc
import chromadb


# @pytest.fixture(scope="session")
# def test_chroma():
#     # Use an ephemeral in-memory ChromaDB for tests
#     client = chromadb.EphemeralClient()
#     print("test_chroma")
#     return client


@pytest.fixture
# def client(test_chroma):
def client():
    print(">>> entering client fixture")

    # # Override the dependency to use our ephemeral test DB
    # def get_test_collection():
    #     return test_chroma.get_or_create_collection("test_docs")

    # def get_test_client():
    #     print("get_test_client")
    #     return test_chroma

    # # We also need to override the client getter if used in tasks
    # app.dependency_overrides[chroma_collections.get_docs_collection] = (
    #     get_test_collection
    # )
    # app.dependency_overrides[chroma_collections.get_chroma_client] = get_test_client

    print(">>> before TestClient")
    with TestClient(app) as c:
        print("TestClient is yield")
        yield c
    # app.dependency_overrides.clear()
    print(">>> after TestClient")


# @pytest.fixture(autouse=True)
# def get_test_chroma_client(monkeypatch):
#     def get_test_client():
#         print("get_test_client monkeypatch")
#         return test_chroma

#     # monkeypatch.setattr(
#     #     "app.dependencies.chroma_collections.get_chroma_client", get_test_client
#     # )
#     monkeypatch.setattr(
#         chroma_collections, "get_chroma_client", get_test_client
#     )


# @pytest.fixture(autouse=True)
# def get_test_chroma_collection(monkeypatch, test_chroma):
#     def get_test_collection():
#         print("get_test_collection monkeypatch")
#         return test_chroma.get_or_create_collection(
#             "test_docs", embedding_function=DefaultEmbeddingFunction()
#         )

#     # monkeypatch.setattr(
#     #     "app.dependencies.chroma_collections.get_docs_collection", get_test_collection
#     # )
#     monkeypatch.setattr(
#         chroma_collections, "get_docs_collection", get_test_collection
#     )


@pytest.fixture(autouse=True)
def eager_celery(monkeypatch):
    print("eager_celery")
    # Force Celery tasks to run synchronously during tests
    monkeypatch.setattr("app.tasks.celery_app.conf.task_always_eager", True)
    monkeypatch.setattr("app.tasks.celery_app.conf.task_eager_propagates", True)


# send_task() do not respects eager mode, so replace it with delay(), which does
@pytest.fixture(autouse=True)
def patch_celery_send_task(monkeypatch):
    def fake_send_task(name, args=None, kwargs=None, **options):
        if name == "process_uploaded_doc":
            return process_uploaded_doc.delay(*(args or ()), **(kwargs or {}))
        raise ValueError(f"Unexpected task name: {name}")

    monkeypatch.setattr(celery_app, "send_task", fake_send_task)
