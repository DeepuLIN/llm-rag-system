from functools import lru_cache
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    VECTOR_DB_DIR,
    ensure_directories,
)
from src.rag.loader import load_markdown_documents


@lru_cache(maxsize=1)
def get_embedding_function() -> HuggingFaceEmbeddings:
    """
    Create and cache the HuggingFace embedding model.
    Force CPU to avoid CUDA OOM on small GPUs.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split loaded documents into smaller chunks for better retrieval.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_vectorstore() -> Chroma:
    """
    Load markdown docs, split them into chunks, embed them,
    and persist them into ChromaDB.
    """
    ensure_directories()

    documents = load_markdown_documents()
    chunks = split_documents(documents)
    embedding_function = get_embedding_function()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=COLLECTION_NAME,
    )

    return vectorstore


@lru_cache(maxsize=1)
def load_vectorstore() -> Chroma:
    """
    Load and cache an existing persistent Chroma vector store.
    """
    ensure_directories()

    embedding_function = get_embedding_function()

    vectorstore = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embedding_function,
        collection_name=COLLECTION_NAME,
    )
    return vectorstore


if __name__ == "__main__":
    print("Building vector store...")
    vectorstore = build_vectorstore()
    count = vectorstore._collection.count()
    print(f"Vector store created successfully with {count} chunks.")