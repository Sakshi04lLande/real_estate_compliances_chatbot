# core/rag.py

import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import AzureChatOpenAI

load_dotenv()

CHROMA_DIR = "chroma_db"

# Embeddings
embed_model = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)
embeddings = HuggingFaceEmbeddings(model_name=embed_model)

# Vector store
vectordb = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings,
)

retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# Azure OpenAI LLM
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    temperature=0,
)
