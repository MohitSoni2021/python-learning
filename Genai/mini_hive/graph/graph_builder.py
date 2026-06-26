"""Graph builder for assembling workflow."""

from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import planner_node, research_node, writer_node, judge_node
from graph.edges import judge_decision

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("research", research_node)
    builder.add_node("writer", writer_node)
    builder.add_node("judge", judge_node)

    builder.set_entry_point("planner")

    builder.add_edge("planner", "research")
    builder.add_edge("research", "writer")
    builder.add_edge("writer", "judge")

    # 🔥 THIS PART MUST BE EXACT
    builder.add_conditional_edges(
        "judge",
        judge_decision,
        {
            "retry": "research",
            "end": END
        }
    )

    return builder.compile()