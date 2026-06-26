"""Web search tool implementation."""
from tools.base_tool import BaseTool
class SearchTool(BaseTool):
    name = "search"
    description = "Search general information"

    def run(self, query: str):
        return f"""
            Topic: {query}

            Definition:
            Data refers to raw facts and information.

            Types:
            - Qualitative data (descriptive)
            - Quantitative data (numerical)

            Examples:
            - Business reports
            - Scientific experiments
            - Personal records

            Use this information to answer properly.
            """