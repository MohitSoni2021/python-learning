from typing_extensions import TypedDict
from typing import Annotated, Optional, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="http://localhost:11434/v1",
)

class State(TypedDict):
    user_query : str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("\n\nBOT : \t", state)
    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[{"role":"user", "content":state.get("user_query")}]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def eval_res(state: State) -> Literal["chatbot_adv", "endnode"]:
    if False:
        return "endnode"
    return "chatbot_adv"

def endnode(state: State):
    print("\n\nBOT_END : \t", state)
    return state

def chatbot_adv(state: State):
    print("\n\nBOT_ADV : \t", state)
    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[{"role":"user", "content":state.get("user_query")}]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_adv", chatbot_adv)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", eval_res)

graph_builder.add_edge("chatbot_adv", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()
updated_state = graph.invoke(State({ "user_query": "\n\nHey, what is 2 + 2 ?" }))

print(updated_state)
