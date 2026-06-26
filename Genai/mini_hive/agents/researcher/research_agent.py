"""Research agent implementation."""
from agents.base_agent import BaseAgent
from tools.tool_registry import TOOLS

class ResearchAgent(BaseAgent):
    def run(self, query: str):
        # 🔥 Step 1: Ask LLM for structured decision
        decision_prompt = f"""
            You are an intelligent agent.

            Available tools:
            - weather → for weather queries
            - search → for general knowledge

            User query: {query}

            STRICT RULES:
            - Only choose from: weather, search, none
            - Return ONLY JSON
            - No explanation

            Format:
            {{
                "tool": "weather/search/none",
                "input": "string"
            }}
            """

        # ✅ IMPORTANT: use BaseAgent.run (not llm.invoke)
        decision = super().run(decision_prompt, json_mode=True)

        print("\n[Agent Decision JSON]\n", decision)

        # 🔥 Step 2: Extract safely
        tool = decision.get("tool", "none")
        tool_input = decision.get("input", "").strip()

        if not tool_input or len(tool_input.split()) > 10:
            tool_input = query

        # 🔥 Step 3: Execute tool
        if tool in TOOLS:
            print(f"\n[Using Tool]: {tool}")
            return TOOLS[tool].run(tool_input)

        # 🔥 Step 4: fallback to LLM
        print("\n[Fallback to LLM]")
        return super().run(query)