"""Judge agent implementation."""

from agents.base_agent import BaseAgent

class JudgeAgent(BaseAgent):
    def run(self, query: str, answer: str):
        prompt = f"""
        You are a strict evaluator.

        User Query:
        {query}

        Answer:
        {answer}

        Evaluate:
        - Accuracy
        - Completeness
        - Clarity

        Return JSON:
        {{
            "score": number (1-10),
            "feedback": "short reason"
        }}
        """

        return super().run(prompt, json_mode=True)