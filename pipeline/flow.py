# pipeline/flow.py
from dataclasses import dataclass
from livekit.agents import Agent, AgentSession, JobContext
from livekit.plugins import openai
from tools.weather import tool_weather
from tools.booking import tool_booking
from tools.end_call import tool_end_call

@dataclass
class AgentUserData:
    job: JobContext

class RestaurantAgent(Agent):
    def __init__(self, userdata: AgentUserData):
        super().__init__(
            instructions=(
                "Bạn là trợ lý đặt bàn nhà hàng."
            ),
            tools=[tool_weather, tool_booking, tool_end_call],
            llm=openai.LLM(model="gpt-4o-mini"),
        )
        self._userdata = userdata

    @property
    def userdata(self):
        return self._userdata


async def build_session(ctx: JobContext) -> AgentSession:
    return AgentSession(
        stt=openai.STT(model="gpt-4o-mini"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(model="gpt-4o-mini"),
        userdata=AgentUserData(job=ctx),
    )
