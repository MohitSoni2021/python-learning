"""Service layer for running agents."""

from graph.graph_builder import build_graph

graph = build_graph()

def run_agent(query: str):
    result = graph.invoke({
        "user_input": query
    })

    return result["final_output"]