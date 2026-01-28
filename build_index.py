# build_index.py

import os
from dotenv import load_dotenv


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

PDF_DIR = "pdfs"
CHROMA_DIR = "chroma_db"


def load_all_pdfs(pdf_dir: str):
    docs = []
    for root, _, files in os.walk(pdf_dir):
        for f in files:
            if f.lower().endswith(".pdf"):
                path = os.path.join(root, f)
                print(f"📄 Loading {path} ...")
                loader = PyPDFLoader(path)
                file_docs = loader.load()

                for d in file_docs:
                    d.metadata = d.metadata or {}
                    d.metadata["source_file"] = f

                docs.extend(file_docs)
    return docs


def main():
    os.makedirs(PDF_DIR, exist_ok=True)

    print("📚 Loading PDFs...")
    docs = load_all_pdfs(PDF_DIR)
    print(f"Total pages loaded: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks: {len(chunks)}")

    embed_model = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )
    embeddings = HuggingFaceEmbeddings(model_name=embed_model)

    if os.path.exists(CHROMA_DIR):
        print("⚠️ Existing Chroma DB detected. Overwriting...")
        import shutil
        shutil.rmtree(CHROMA_DIR)

    print("💾 Creating Chroma DB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )

    print("✅ Done — Chroma DB saved at:", CHROMA_DIR)


if __name__ == "__main__":
    main()
