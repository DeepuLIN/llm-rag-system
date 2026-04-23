from src.graph.state import GraphState
from src.rag.rag_chain import answer_query


def rag_node(state: GraphState) -> GraphState:
    query = state.get("query", "").strip()
    trace = state.get("trace", [])

    if not query:
        return {
            **state,
            "error": "Empty query received in rag_node.",
            "answer": "No query was provided.",
            "trace": trace + [
                {
                    "step": "rag_node",
                    "status": "failed",
                    "reason": "empty query",
                }
            ],
        }

    try:
        history = state.get("history", [])
        result = answer_query(query, history=history)

        rewritten_query = result.get("rewritten_query", query)
        retrieved_sources = result.get("retrieved_sources", [])
        context = result.get("context", "")
        answer = result.get("answer", "I could not find that in the knowledge base.")

        return {
            **state,
            "rewritten_query": rewritten_query,
            "retrieved_docs": result.get("documents", []),
            "retrieved_sources": retrieved_sources,
            "context": context,
            "answer": answer,
            "trace": trace + [
                {
                    "step": "rag_node",
                    "input_query": query,
                    "rewritten_query": rewritten_query,
                    "retrieved_sources": retrieved_sources,
                    "context_preview": context[:500],
                    "answer": answer,
                }
            ],
        }

    except Exception as exc:
        import traceback
        traceback.print_exc()

        return {
            **state,
            "error": str(exc),
            "answer": f"An error occurred while processing the query: {exc}",
            "trace": trace + [
                {
                    "step": "rag_node",
                    "status": "failed",
                    "error": str(exc),
                }
            ],
        }