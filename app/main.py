# https://techstrong.ai/articles/an-ai-powered-document-search-app-with-chroma/
# https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0
# https://docs.trychroma.com/integrations/embedding-models/ollama

import os
import pathlib

# from fastapi import FastAPI, File, UploadFile
import fastapi

import chromadb
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

# from langchain_ollama import OllamaEmbeddings, OllamaLLM

LLM_MODEL = "embeddinggemma"
DATA_DIRECTORY = pathlib.Path("data")
# Adjust the base URL as per your Ollama server configuration
OLLAMA_URL = "http://ollama:11434"


def load_txt_files(directory):
    txt_files = []
    names = []

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            names.append(filename)
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                txt_files.append(file.read())
    return (txt_files, names)


app = fastapi.FastAPI()

chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection(
    name="wiki",
    embedding_function=OllamaEmbeddingFunction(
        model_name=LLM_MODEL,
        url=OLLAMA_URL,
    ),
)
# docs, ids = load_txt_files("./data/docs")

# collection.add(documents=docs, ids=ids)

# done = False
# while not done:
#     query = input("What are you searching for? (or Q to quit) ")
#     if query == "Q":
#         done = True
#     else:
#         results = collection.query(query_texts=[query], n_results=3)
#         print({"ids": results["ids"], "distances": results["distances"]})


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/search")
def search_docs(query: str):
    return collection.query(query_texts=[query], n_results=30)


@app.post("/upload")
def upload_doc(file: fastapi.UploadFile):
    if not file.content_type == "text/plain":
        raise fastapi.HTTPException(status_code=400, detail="Not supported file type")

    contents = file.file.read()

    try:
        with open(DATA_DIRECTORY / "docs" / file.filename, "wb") as f:
            f.write(contents)

    except Exception:
        raise fastapi.HTTPException(
            status_code=500, detail="Error occured during saving the uploaded file"
        )
    finally:
        file.file.close()

    try:
        collection.add(documents=[contents.decode("utf-8")], ids=[file.filename]) # TODO: винести в окрему функцію
    except Exception:
        raise fastapi.HTTPException(
            status_code=500, detail="Error occured during processing the uploaded file"
        )
    # collection.add(documents=[contents.decode("utf-8")], ids=[file.filename])
    
    return {"message": f"File {file.filename} was successfuly uploaded"}
