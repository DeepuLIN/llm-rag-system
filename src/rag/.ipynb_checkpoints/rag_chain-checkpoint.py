from typing import List, Optional

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from src.rag.config import OLLAMA_BASE_URL, OLLAMA_MODEL, TOP_K
from src.rag.retriever import retrieve_documents


def get_llm() -> ChatOllama:
    return ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    )


llm = get_llm()


def format_context(documents: List[Document]) -> str:
    parts = []

    for doc in documents:
        source = doc.metadata.get("relative_path", "unknown")
        content = (doc.page_content or "").strip()
        if content:
            parts.append(f"Source: {source}\n{content}")

    return "\n\n".join(parts)


def rewrite_query_with_history(question: str, history=None) -> str:
    if not history:
        return question

    history_text = "\n".join(h for h in history if isinstance(h, str)).strip()
    if not history_text:
        return question

    prompt = f"""
Rewrite the user's latest question into a standalone question.
Return only the rewritten question and nothing else.

Conversation history:
{history_text}

Current question:
{question}

Rewritten question:
""".strip()

    response = llm.invoke(prompt)
    rewritten = str(response.content).strip().strip('"').strip("'")

    prefixes_to_remove = [
        "Here is the rewritten question:",
        "Rewritten question:",
        "Standalone question:",
    ]

    for prefix in prefixes_to_remove:
        if rewritten.lower().startswith(prefix.lower()):
            rewritten = rewritten[len(prefix):].strip()

    return rewritten or question


SYSTEM_PROMPT = """
You are a grounded assistant.

Rules:
- Answer only from the provided context.
- If the question asks for more details, summarize the most relevant details from the retrieved context.
- Keep the answer short and factual.
- If the answer is not in the context, say exactly:
I could not find that in the knowledge base.
""".strip()


def answer_query(query: str, history: Optional[List[str]] = None, k: int = TOP_K) -> dict:
    rewritten_query = rewrite_query_with_history(query, history)
    retrieved_docs = retrieve_documents(rewritten_query, k=k)
    context = format_context(retrieved_docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                """
Context:
{context}

Question:
{question}

Answer:
""".strip(),
            ),
        ]
    )

    messages = prompt.invoke(
        {
            "context": context,
            "question": query,
        }
    )

    response = llm.invoke(messages)
    answer = str(response.content).strip()

    return {
        "question": query,
        "rewritten_query": rewritten_query,
        "documents": retrieved_docs,
        "retrieved_sources": [
            doc.metadata.get("relative_path", "unknown") for doc in retrieved_docs
        ],
        "context": context,
        "answer": answer,
    }