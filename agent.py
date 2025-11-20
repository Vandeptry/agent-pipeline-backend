# agent.py
import asyncio
from livekit import agents
from pipeline.flow import build_session, RestaurantAgent


async def entrypoint(ctx: agents.JobContext):
    print(f"[AGENT] New job for room: {ctx.room.name}")

    await ctx.connect()
    session = await build_session(ctx)
    agent = RestaurantAgent(session.userdata)

    async with session:
        await session.start(room=ctx.room, agent=agent)
        await session.say("Xin chào, tôi là trợ lý nhà hàng. Bạn cần hỗ trợ điều gì ạ?")
        await asyncio.Event().wait()


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
