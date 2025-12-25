# https://techstrong.ai/articles/an-ai-powered-document-search-app-with-chroma/
# https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0
# https://docs.trychroma.com/integrations/embedding-models/ollama

# TODO: Реалізувати вилучення документу

import fastapi
from .dependencies import chroma_collections


from . import config
from .docs_processing import docs_saving

app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def search_docs(
    query: str, docs_collection=fastapi.Depends(chroma_collections.get_docs_collection)
):
    return docs_collection.query(query_texts=[query], n_results=30)


@app.post("/upload")
def upload_doc(
    file: fastapi.UploadFile,
    docs_collection=fastapi.Depends(chroma_collections.get_docs_collection),
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

    return {"message": f"File {file.filename} was successfuly uploaded"}
