from openai import OpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from typing_extensions import TypedDict
from typing import Annotated, Optional, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from openai import OpenAI
import json

import requests


from rich.console import Console
from rich.markdown import Markdown

from config.openAI_Client import chat_OpenAI_Agent
from prompts.system_prompt import SYSTEM_PROMPT
from output_struct.output_struct import StructuredOutput


class State(TypedDict):
    user_query: str
    tool_name: Optional[str]
    tool_input: Optional[str]
    tool_output: Optional[str]
    final_answer: Optional[str]
    is_tool_required: bool
    error_type: Optional[str]

def reasoning_node(state: State):
    user_query = state["user_query"]
    
    print("\n👤 : ", user_query)
    print("\n : using reasoning_node.")

    response = chat_OpenAI_Agent(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        properties={
            "response_format": StructuredOutput
        }
    )
    
    print("\n🤖 :  Reasoning about the user query...")
    print(f"\n{response.choices[0].message.parsed}")

    parsed = response.choices[0].message.parsed

    state["tool_name"] = parsed.tool_name
    state["tool_input"] = parsed.tool_input
    state["is_tool_required"] = parsed.is_tool_required
    state["final_answer"] = parsed.final_answer
    state["error_type"] = parsed.error_type

    return state

# decide if there is any requirement of the tool or not.
def should_use_tool(state: State):
    print("\n🔍 :  Deciding whether to use tool or not... by shoud_use_tool.")
    if state["error_type"] == "user_error":
        return "ask_user_node"

    query = state["user_query"].lower()

    if "weather" in query:
        return "tool_node"

    if state["is_tool_required"]:
        return "tool_node"

    return "final_node"


# this node have the tool level access
def tool_node(state: State):
    print("\n🔧 :  Using tool_node to get the weather information...")
    if state["tool_name"] == "get_weather":

        city = state["tool_input"]

        try:

            result = requests.get(
                f"https://wttr.in/{city}?format=%C+%t",
                timeout=5
            ).text

            state["tool_output"] = result

            # USER ERROR (wrong city)
            if "Unknown location" in result or "Sorry" in result:
                state["error_type"] = "user_error"

            else:
                state["error_type"] = None

        except requests.exceptions.RequestException:

            # SYSTEM ERROR (api fail / network / rate limit)
            state["tool_output"] = None
            state["error_type"] = "system_error"

    return state


def final_node(state: State):
    print("\n✅ :  Arriving at final_node to generate the final answer for the user query...")
    prompt = f"""
        User query: {state['user_query']}
        Tool output: {state['tool_output']}
    """

    response = chat_OpenAI_Agent(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ],
        properties={}
    )

    state["final_answer"] = response.choices[0].message.content

    return state

def after_tool_router(state: State):
    print("\n🔧: calling... after_tool_router.")
    # print("\n🔧 :  Tool output:", state["tool_output"])
    # print("\n🔍 :  Analyzing tool output...")
    # print("\n🧠 :  Reasoning about the tool output...")
    # print(f"\n🪲 :  {state['error_type']}")

    if state["error_type"] == "user_error":
        return "ask_user_node"

    if state["error_type"] == "system_error":
        return "tool_unavailable_node"

    return "final_node"

# if input is not correct 
def ask_user_node(state: State):
    print("\n❌ :  Calling ask_user_node to get correct city name from the user...")
    print("\n❌ City not found.")

    new_city = input("Please enter a valid city name: ")

    state["tool_input"] = new_city
    state["error_type"] = None

    return state

def tool_unavailable_node(state: State):

    state["final_answer"] = (
        "⚠️ Weather service is temporarily unavailable. "
        "Please try again later."
    )

    return state

def chatbot(state: State):
    user_query = state.get("user_query")

    system_prompt = SYSTEM_PROMPT
    
    response = chat_OpenAI_Agent(
        model="qwen2.5:7b",
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_query}
        ],
        properties={
            "response_format": StructuredOutput
        }
    )

    state["llm_output"] = response.choices[0].message.parsed
    return state

def endnode(state: State):
    return state



graph_builder = StateGraph(State)

graph_builder.add_node("reasoning", reasoning_node)
graph_builder.add_node("tool_node", tool_node)
graph_builder.add_node("final_node", final_node)
graph_builder.add_node("ask_user_node", ask_user_node)
graph_builder.add_node("tool_unavailable_node", tool_unavailable_node)

graph_builder.add_edge(START, "reasoning")

graph_builder.add_conditional_edges(
    "reasoning",
    should_use_tool
)

# After tool execution decide what to do
graph_builder.add_conditional_edges(
    "tool_node",
    after_tool_router,
    {
        "ask_user_node": "ask_user_node",
        "tool_unavailable_node": "tool_unavailable_node",
        "final_node": "final_node"
    }
)

# If user fixes city → retry tool
graph_builder.add_edge("ask_user_node", "reasoning")

# Final answer
graph_builder.add_edge("final_node", END)

# Tool unavailable → end
graph_builder.add_edge("tool_unavailable_node", END)

graph = graph_builder.compile()

# this is the starting point of the agent workflow.
def init_chatbot(query: str):

    initial_state = {
        "user_query": query,
        "tool_name": None,
        "tool_input": None,
        "tool_output": None,
        "final_answer": None,
        "is_tool_required": False,
        "error_type": None
    }

    # whole workflow will be executed by invoking the graph with the initial state.
    updated_state = graph.invoke(initial_state)

    # This is going to return the final answer to the user query after executing the whole workflow.
    return updated_state["final_answer"]


getting_user_query_input = input("👉️ : \t")


# print(json.dumps(init_chatbot(getting_user_query_input)))
console = Console()
markdown = Markdown(f"\n\n{init_chatbot(getting_user_query_input)}")

console.print(markdown)