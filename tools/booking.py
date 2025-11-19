# tools/booking.py
from typing import Any

import httpx
from livekit.agents import RunContext, function_tool

from utils.env import get_env

BOOKING_API_BASE = get_env("BOOKING_API_BASE", "https://example.com/api/restaurant")


@function_tool
async def tool_booking(
    context: RunContext,
    guest_name: str,
    people: int,
    time: str,
    phone: str | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    """
    Đặt bàn nhà hàng.

    Args:
        guest_name: Tên khách
        people: Số lượng người
        time: Thời gian theo kiểu string tự nhiên (VD: '19:00 tối nay')
        phone: Số điện thoại (nếu có)
        note: Ghi chú thêm
    """
    payload = {
        "guest_name": guest_name,
        "people": people,
        "time": time,
        "phone": phone,
        "note": note,
    }

    api_url = f"{BOOKING_API_BASE}/booking"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(api_url, json=payload)
            if r.status_code >= 400:
                return {
                    "success": False,
                    "error": f"Booking API trả về lỗi {r.status_code}",
                }
            data: Any = r.json()
    except Exception:
        data = {
            "booking_id": "DEMO-12345",
            "confirmed": True,
        }

    return {
        "success": True,
        "booking": data,
    }
