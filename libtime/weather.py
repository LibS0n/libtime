import logging
from typing import Optional, Dict, Any

import aiohttp

from .core import resolve_city

logger = logging.getLogger(__name__)

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    51: "Light drizzle",
    61: "Rain",
    71: "Snowfall",
    80: "Showers",
    95: "Thunderstorm",
}

async def get_current_weather(city_name: str) -> Optional[Dict[str, Any]]:
    data = resolve_city(city_name)
    if not data:
        return None

    lat = data["lat"]
    lng = data["lng"]
    tz = data["tz"]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lng,
        "current_weather": "true",
        "timezone": tz,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=5) as resp:
                if resp.status == 200:
                    payload = await resp.json()
                    current = payload.get("current_weather", {})
                    return {
                        "temperature": current.get("temperature"),
                        "windspeed": current.get("windspeed"),
                        "weathercode": current.get("weathercode"),
                        "time": current.get("time"),
                        "city": city_name,
                        "timezone": tz,
                    }
                else:
                    logger.warning(f"Open-Meteo returned {resp.status} for {city_name}")
    except Exception as e:
        logger.warning(f"Weather request failed for {city_name}: {e}")

    return None

def format_weather(weather: Dict[str, Any]) -> str:
    temp = weather["temperature"]
    code = weather["weathercode"]
    desc = WEATHER_CODES.get(code, f"Code {code}")
    return f"{desc}, {temp:.1f}°C"