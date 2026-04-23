from typing import List, TypedDict, Optional, Dict, Any

from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    query: str
    history: List[str]

    route: str
    rewritten_query: str
    retrieved_docs: List[Document]
    retrieved_sources: List[str]
    context: str
    answer: str
    final_answer: str
    error: Optional[str]

    trace: List[Dict[str, Any]]