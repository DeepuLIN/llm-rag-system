from src.graph.state import GraphState


def router_node(state: GraphState) -> GraphState:
    query = state.get("query", "").strip()
    trace = state.get("trace", [])

    if not query:
        return {
            **state,
            "route": "final",
            "error": "Empty query provided.",
            "final_answer": "No query was provided.",
            "trace": trace + [
                {
                    "step": "router",
                    "input_query": query,
                    "route": "final",
                    "reason": "empty query",
                }
            ],
        }

    return {
        **state,
        "route": "rag",
        "trace": trace + [
            {
                "step": "router",
                "input_query": query,
                "route": "rag",
            }
        ],
    }