"""Weather tool implementation."""

import requests
from tools.base_tool import BaseTool

class WeatherTool(BaseTool):
    name = "weather"
    description = "Get weather of a city"

    def run(self, city: str):
        url = f"https://wttr.in/{city}?format=%C+%t"
        return requests.get(url).text