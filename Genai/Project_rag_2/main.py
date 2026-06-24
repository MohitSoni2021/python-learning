from typing_extensions import TypedDict
from typing import Optional

from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage
)

import uuid

from tools.weather_tool import get_weather
from prompts.system_prompt import SYSTEM_PROMPT
from output_struct.output_struct import StructuredOutput

from tools.tools_provider import avaliable_tools



llm = ChatOllama(
    model="mistral:7b",
    temperature=0.3
)

struct_llm = llm.with_structured_output(StructuredOutput)

class State(TypedDict):
    user_query: str
    tool_name: Optional[str]
    tool_input: Optional[str]
    tool_output: Optional[str]
    final_answer: Optional[str]
    is_tool_required: bool
    error_type: Optional[str]
    messages: list
    is_final: bool
    step_count: int


def reasoning_node(state: State):

    print("\n🧠 Reasoning Step:", state["step_count"])

    res = struct_llm.invoke(state["messages"])
    
    if res.final_answer:
        state["messages"].append(
            AIMessage(content=res.final_answer)
        )

    state["tool_name"] = res.tool_name
    state["tool_input"] = res.tool_input
    state["tool_output"] = res.tool_output
    if res.final_answer is not None:
        state["final_answer"] = res.final_answer
    state["is_tool_required"] = res.is_tool_required
    state["error_type"] = res.error_type
    
    state["is_final"] = bool(res.final_answer and not res.is_tool_required)

    state["step_count"] += 1

    return state


def tool_node(state: State):

    tool_name = state["tool_name"]
    tool_input = state["tool_input"]

    print("\n🔧 Tool Selected:", tool_name)
    print("Input:", tool_input)
    
    tool = avaliable_tools.get(tool_name)
    
    print("Tool Function:", tool)
    
    if tool is None:
        print("❌ Tool not found")
        return state
    
    tool_output = tool.invoke(tool_input)
    
    print("\n🛠 Tool Output:\n", tool_output)

    state["tool_output"] = tool_output
    
    state["messages"].append(
        ToolMessage(
            content=str(tool_output),
            name=tool_name,
            tool_call_id=str(uuid.uuid4())
        )
    )

    return state

def router(state: State):

    if state["step_count"] > 5:
        print("\n⚠️ Max reasoning steps reached.")
        return "end"
    
    if state["tool_output"] is not None:
        return "end"

    if state["is_final"]:
        return "end"

    if state["is_tool_required"]:
        return "tool_node"

    return "end"

def humanresponse_node(state: State):
    
    pass

graph = StateGraph(State)

graph.add_node("reasoningNode", reasoning_node)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "reasoningNode")

graph.add_conditional_edges(
    "reasoningNode",
    router,
    {
        "tool_node": "tool_node",
        "end": END
    }
)

graph.add_edge("tool_node", "reasoningNode")

final_graph = graph.compile()

if __name__ == "__main__":
    conversation_history = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]
    
    while True:

        user_query = input("\nEnter your query (or 'exit'): ")

        if user_query.lower() == "exit":
            break

        conversation_history.append(HumanMessage(content=user_query))
        initial_state = State(
            user_query=user_query,
            tool_name=None,
            tool_input=None,
            tool_output=None,
            final_answer=None,
            is_tool_required=False,
            error_type=None,
            is_final=False,
            step_count=0,
            messages=conversation_history.copy()
        )

        print("\n🚀 Running ReAct Agent...\n")

        output = final_graph.invoke(initial_state)

        print("\n🤖 Final Answer:\n")
        print(output["final_answer"])
        print("\n")
        
        conversation_history = output["messages"]