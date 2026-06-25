from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langgraph.checkpoint.mongodb import MongoDBSaver

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

graph_builder = StateGraph(State)

# adding nodes to the graph builder
graph_builder.add_node("chatbot", chatbot)

# creating edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
# START -> chatbot -> END

graph = graph_builder.compile()

# adding check point
def compile_checkpoint_with_mongodb(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)
    

MONGO_URI="mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(MONGO_URI) as checkpointer:
    
    graph_with_checkpointer = compile_checkpoint_with_mongodb(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "Mohit"
        }
    }

    for chunk in graph_with_checkpointer.stream(
        State({ "message": ["Tell me everything about me you know."] }),
        config=config,
        stream_mode="values"
    ):
        chunk["message"][-1].pretty_print()

    

    # checkpointer (Mohit) = Hey, My name is Mohit Soni
