# agent2.py
from utils.env import load_dotenv
load_dotenv()

import asyncio
import aiohttp
from livekit import agents
from livekit.agents import stt, tts

from pipeline.flow2 import build_session


async def entrypoint(ctx: agents.JobContext):
    print(f"[AGENT2] New job for room: {ctx.room}")

    await ctx.connect()
    session = await build_session(ctx)

    async with session:
        await session.start(room=ctx.room)
        await session.say("Xin chào, tôi là trợ lý mới. Bạn cần hỗ trợ gì không?")

        async for evt in session.listen():
            if evt.type == "stt.transcription" and evt.text:
                user_text = evt.text
                print("[USER]:", user_text)

                # Gọi LLM qua flow2
                reply = await session.userdata["llm_fn"](user_text)
                print("[AGENT]:", reply)

                await session.say(reply)

        await asyncio.Event().wait()


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
