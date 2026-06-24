import requests
from langchain_core.tools import tool

API_KEY = "6dbaf94a16b79a0f3f87f30509fd3b2e"

@tool
def get_weather(city: str):
    """
    Get the current weather for a given city using the OpenWeatherMap API.
    """

    try:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        res = requests.get(url, timeout=10)
        data = res.json()

        if res.status_code != 200:
            return f"Weather API error: {data.get('message', 'Unknown error')}"

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        weather_desc = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        return (
            f"Weather in {city}:\n"
            f"Condition: {weather_desc}\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

    except Exception as e:
        return f"Weather API error: {str(e)}"