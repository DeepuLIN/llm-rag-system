from functools import lru_cache
from typing import List, Optional, Any

from fastapi import FastAPI
from pydantic import BaseModel




app = FastAPI(title="Agentic RAG")


@lru_cache(maxsize=1)
def get_graph():
    from src.graph.graph import build_graph
    return build_graph()



# ---------------------------
# Request / Response Schemas
# ---------------------------
class AskRequest(BaseModel):
    query: str
    history: Optional[List[str]] = None


class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    trace: List[Any]


# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def root():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    graph = get_graph()

    result = graph.invoke(
        {
            "query": request.query,
            "history": request.history or [],
            "trace": [],
        }
    )

    sources = result.get("retrieved_sources", [])

    unique_sources = []
    seen = set()
    for source in sources:
        if source not in seen:
            unique_sources.append(source)
            seen.add(source)

    return AskResponse(
        answer=result.get("final_answer", "No answer produced."),
        sources=unique_sources,
        trace=result.get("trace", []),
    )