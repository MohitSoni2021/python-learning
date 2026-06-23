import requests

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"

    res = requests.get(url)

    if res.status_code == 200:
        return f"The weather in {city} is {res.text}"
    else:
        return "Something went wrong"
    
# print(get_weather("goa"))