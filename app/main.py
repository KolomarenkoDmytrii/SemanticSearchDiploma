# https://techstrong.ai/articles/an-ai-powered-document-search-app-with-chroma/
# https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0
# https://docs.trychroma.com/integrations/embedding-models/ollama

import os

from fastapi import FastAPI

import chromadb
from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction,
)

# from langchain_ollama import OllamaEmbeddings, OllamaLLM

LLM_MODEL = "embeddinggemma"
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

app = FastAPI()

chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection(
    name="wiki",
    embedding_function=OllamaEmbeddingFunction(
        model_name=LLM_MODEL,
        url=OLLAMA_URL,
    ),
)
docs, ids = load_txt_files("./data/docs")

collection.add(documents=docs, ids=ids)

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
def read_item(query: str):
    return collection.query(query_texts=[query], n_results=3)
