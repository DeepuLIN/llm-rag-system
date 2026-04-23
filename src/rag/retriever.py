from typing import List

from langchain_core.documents import Document

from src.rag.config import TOP_K
from src.rag.vectorstore import load_vectorstore


def retrieve_documents(query: str, k: int = TOP_K) -> List[Document]:
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=k)


if __name__ == "__main__":
    query = input("Enter your query: ").strip()

    if not query:
        print("No query provided.")
    else:
        docs = retrieve_documents(query)

        print(f"\nRetrieved {len(docs)} documents:\n")
        for i, doc in enumerate(docs, start=1):
            print(f"{i}. {doc.metadata.get('relative_path', 'unknown')}")
            print(doc.page_content[:300])
            print("-" * 80)