# tools/weather.py
import httpx
from typing import Any
from livekit.agents import RunContext, function_tool

API = "https://api.open-meteo.com/v1/forecast"

CITY_MAP = {
    "hanoi": (21.0278, 105.8342),
    "ha noi": (21.0278, 105.8342),
    "saigon": (10.8231, 106.6297),
    "ho chi minh": (10.8231, 106.6297),
    "danang": (16.0471, 108.2068),
    "da nang": (16.0471, 108.2068),
}


@function_tool
async def tool_weather(context: RunContext, location: str) -> dict[str, Any]:
    q = location.strip().lower()

    if q in CITY_MAP:
        lat, lon = CITY_MAP[q]
    else:
        lat, lon = (21.0278, 105.8342)

    async with httpx.AsyncClient(timeout=10) as client:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True,
        }
        try:
            r = await client.get(API, params=params)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            return {
                "success": False,
                "location": location,
                "error": str(e),
            }

    cw = data.get("current_weather", {})
    return {
        "success": True,
        "location": location,
        "temperature": cw.get("temperature"),
        "windspeed": cw.get("windspeed"),
        "weathercode": cw.get("weathercode"),
    }
