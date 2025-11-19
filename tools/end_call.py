# tools/end_call.py
from livekit.agents import RunContext, function_tool


@function_tool
async def tool_end_call(
    context: RunContext,
    reason: str | None = None,
) -> dict[str, str]:
    """
    Kết thúc cuộc gọi. Agent phải:
    1) Nói lời chào / tạm biệt.
    2) Sau đó shutdown job, rời phòng.

    Thực hiện shutdown qua userdata chứa JobContext (set ở agent.py).
    """

    # Bảo agent nói tạm biệt
    await context.session.generate_reply(
        instructions=(
            "Hãy nói lời cảm ơn và chào tạm biệt khách một cách lịch sự, "
            "nhắc lại chi tiết đặt bàn nếu có."
        )
    )

    job_ctx = getattr(context.userdata, "job_ctx", None)
    if job_ctx is not None:
        # Python JobContext có phương thức shutdown tương tự JS :contentReference[oaicite:1]{index=1}
        job_ctx.shutdown(reason or "user_requested_end")

    return {"status": "ended", "reason": reason or "user_requested_end"}
