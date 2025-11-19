# tools/weather.py
from typing import Any

import httpx
from livekit.agents import RunContext, function_tool

from utils.env import get_env

WEATHER_API_BASE = get_env("WEATHER_API_BASE", "https://api.open-meteo.com/v1/forecast")


@function_tool
async def tool_weather(
    context: RunContext,
    location: str,
) -> dict[str, Any]:
    """
    Tra cứu thời tiết hiện tại theo tên địa điểm (city).
    Trả về JSON đơn giản cho LLM đọc.
    """

    # Ví dụ gọi Open-Meteo demo (lat/lon cứng hoặc em custom API riêng)
    # Ở đây anh làm stub rất đơn giản, để tránh phụ thuộc phức tạp.
    # Em có thể thay bằng API nội bộ nhà hàng.
    async with httpx.AsyncClient(timeout=10) as client:
        # TODO: map location -> lat/lon thật. Tạm giả lập:
        params = {
            "latitude": 21.0278,
            "longitude": 105.8342,
            "current_weather": True,
        }
        try:
            r = await client.get(WEATHER_API_BASE, params=params)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            return {
                "success": False,
                "error": f"Không lấy được thời tiết ({e})",
                "location": location,
            }

    cw = data.get("current_weather", {})
    return {
        "success": True,
        "location": location,
        "summary": {
            "temperature": cw.get("temperature"),
            "windspeed": cw.get("windspeed"),
            "weathercode": cw.get("weathercode"),
        },
    }
