"""LangGraph node wrappers."""

from agents.planner.planner_agent import PlannerAgent
from agents.researcher.research_agent import ResearchAgent
from agents.judge.judge_agent import JudgeAgent
from pprint import pprint
from agents.writer.writer_agent import writer_agent

planner = PlannerAgent()
research_agent = ResearchAgent()
judge_agent = JudgeAgent()


def planner_node(state):
    query = state["user_input"]

    result = planner.run(query)

    print("\n[Planner JSON]\n", result)

    return {
        "plan": result.get("steps", [])
    }


def research_node(state):
    query = state["user_input"]
    plan = state.get("plan", [])
    feedback = state.get("feedback", "")

    prompt = f"""
    Task: {query}

    Plan:
    {plan}

    Feedback:
    {feedback}

    Generate improved answer.
    """

    result = research_agent.run(prompt)

    return {
        "research": result
    }


def writer_node(state):
    query = state["user_input"]
    research = state.get("research", "")

    prompt = f"""
You are an expert teacher.

User question:
{query}

Research data:
{research}

Write a HIGH QUALITY answer:
- Clear explanation
- Simple language
- Add examples
- Structure properly (headings, points)

Do NOT repeat raw data.
Explain it.
"""

    result = writer_agent.run(prompt)

    print("\n[Writer Generated Answer]")

    return {
        "final_output": result
    }
    
def judge_node(state):
    query = state["user_input"]
    answer = state["final_output"]

    result = judge_agent.run(query, answer)

    print("\n[Judge JSON]\n", result)

    return {
        "score": result.get("score", 5),
        "feedback": result.get("feedback", "No feedback")
    }