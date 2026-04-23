from langgraph.graph import START, END, StateGraph

from src.graph.state import GraphState
from src.nodes.rag_node import rag_node
from src.nodes.final_node import final_node


def build_graph():
    graph_builder = StateGraph(GraphState)

    graph_builder.add_node("rag", rag_node)
    graph_builder.add_node("final", final_node)

    graph_builder.add_edge(START, "rag")
    graph_builder.add_edge("rag", "final")
    graph_builder.add_edge("final", END)

    return graph_builder.compile()