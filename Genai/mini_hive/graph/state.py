"""LangGraph state definitions."""
from typing import TypedDict

class AgentState(TypedDict):
    user_input: str
    plan: str
    research: str
    final_output: str
    score: int
    feedback: str