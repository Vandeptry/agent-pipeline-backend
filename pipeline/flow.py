# pipeline/flow.py
from dataclasses import dataclass
from livekit.plugins import openai, silero
from livekit.agents import Agent, AgentSession, JobContext

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
                "Bạn là trợ lý nhà hàng nói tiếng Việt. "
                "Nếu người dùng hỏi về thời tiết, hãy gọi tool_weather để trả lời."
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
        stt=openai.STT(model="gpt-4o-mini-transcribe"),
        vad=silero.VAD.load(),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(model="gpt-4o-mini-tts"),
        userdata=AgentUserData(job=ctx),
    )
