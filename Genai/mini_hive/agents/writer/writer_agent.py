"""Writer agent implementation."""
from agents.base_agent import BaseAgent

writer_agent = BaseAgent()

def writer_node(state):
    query = state["user_input"]
    research = state.get("research", "")

    prompt = f"""
You are a professional AI writer.

User question:
{query}

Research data:
{research}

Generate a clear, well-structured answer.
- Explain properly
- Add examples if needed
- Make it easy to understand
"""

    result = writer_agent.run(prompt)

    print("\n[Writer Generated Answer]")

    return {
        "final_output": result
    }