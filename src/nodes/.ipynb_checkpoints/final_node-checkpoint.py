from src.graph.state import GraphState


def final_node(state: GraphState) -> GraphState:
    trace = state.get("trace", [])

    if state.get("error"):
        final_answer = state.get("answer", f"An error occurred: {state.get('error')}")
        return {
            **state,
            "final_answer": final_answer,
            "trace": trace + [
                {
                    "step": "final_node",
                    "final_answer": final_answer,
                    "status": "error",
                }
            ],
        }

    final_answer = state.get("answer", "I could not find that in the knowledge base.")
    return {
        **state,
        "final_answer": final_answer,
        "trace": trace + [
            {
                "step": "final_node",
                "final_answer": final_answer,
                "status": "success",
            }
        ],
    }