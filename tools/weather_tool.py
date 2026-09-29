import requests
from core.tool_registry import tool
from config import WEATHER_API_KEY


@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    try:
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}
        resp = requests.get(url, params=params, timeout=5)
        d = resp.json()
        if resp.status_code == 200:
            return (
                f"{city}: {d['main']['temp']}°C, "
                f"{d['weather'][0]['description']}, "
                f"Humidity {d['main']['humidity']}%"
            )
        return f"Weather unavailable for {city}"
    except Exception as e:
        return f"❌ Error: {e}"
