"""Planner agent implementation."""


from agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def run(self, query: str):
        prompt = f"""
        Break this task into steps.

        Task: {query}

        STRICT RULES:
        - Output ONLY JSON
        - No explanation
        - No markdown
        - No text outside JSON

        Format:
        {{
            "steps": ["step1", "step2", "step3"]
        }}
        """

        return super().run(prompt, json_mode=True)