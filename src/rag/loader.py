from pathlib import Path
from typing import List

from langchain_core.documents import Document

from src.rag.config import KNOWLEDGE_BASE_DIR


def load_markdown_documents(base_dir: Path = KNOWLEDGE_BASE_DIR) -> List[Document]:
    """
    Load all markdown files from the knowledge base directory recursively.

    Each markdown file is loaded as one LangChain Document with metadata.
    """
    documents: List[Document] = []

    if not base_dir.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {base_dir}")

    for file_path in base_dir.rglob("*.md"):
        try:
            text = file_path.read_text(encoding="utf-8").strip()

            if not text:
                continue

            relative_path = file_path.relative_to(base_dir)

            document = Document(
                page_content=text,
                metadata={
                    "source": str(file_path),
                    "relative_path": str(relative_path),
                    "filename": file_path.name,
                    "folder": file_path.parent.name,
                },
            )
            documents.append(document)

        except Exception as exc:
            print(f"Skipping {file_path} due to error: {exc}")

    return documents


if __name__ == "__main__":
    docs = load_markdown_documents()
    print(f"Loaded {len(docs)} documents.\n")

    for i, doc in enumerate(docs[:5], start=1):
        print(f"Document {i}")
        print(f"Filename: {doc.metadata['filename']}")
        print(f"Folder: {doc.metadata['folder']}")
        print(f"Relative Path: {doc.metadata['relative_path']}")
        print(f"Preview: {doc.page_content[:200]}")
        print("-" * 60)