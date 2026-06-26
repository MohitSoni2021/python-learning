"""Base agent abstractions and shared logic."""
from models.llm_provider import get_olllama_client
import json
import re

class BaseAgent:
    def __init__(self, model="llama3.1:8b"):
        self.llm = get_olllama_client(model)
        
    def extract_json(self, text: str):
        try:
            # 🔥 Extract JSON block using regex
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print("[JSON EXTRACT ERROR]", e)

        return {}

    def run(self, prompt: str, json_mode: bool = False):
        if json_mode:
            prompt += "\n\nReturn ONLY valid JSON."

        response = self.llm.invoke(prompt).content

        if json_mode:
            try:
                return json.loads(response)
            except:
                print("\n[JSON PARSE ERROR]\n", response)
                return {}

        return response