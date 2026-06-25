from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

class State(TypedDict):
    message: Annotated[list, add_messages ]

# creating nodes
def chatbot(state: State):
    res = llm.invoke(state.get("message"))
    return { "message" : [res] }

def samplenode(state: State):
    print(f"\n\nInside the sample node -> ", state)
    return { "message" : ["Hey, this is a sample node."] }

graph_builder = StateGraph(State)

# adding nodes to the graph builder
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

# creating edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)
# START -> chatbot -> samplenode -> END

graph = graph_builder.compile()
updated_state = graph.invoke(State({ "message": ["Hi, My name is Mohit Soni."] }))

print(f"\n\nUpdated State => ", updated_state)
