# pipeline/flow2.py
from livekit.plugins import openai
from livekit.agents import AgentSession, JobContext
from livekit.agents import tts
import aiohttp
import os


GROQ_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_KEY = os.getenv("GOOGLE_AI_KEY")
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")


async def llm_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý thân thiện."},
            {"role": "user", "content": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as res:
            data = await res.json()
            return data["choices"][0]["message"]["content"]


async def llm_google(prompt: str) -> str:
    from google import genai
    client = genai.Client(api_key=GOOGLE_KEY)
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=prompt,
    )
    return response.text


async def build_session(ctx: JobContext):

    if GROQ_KEY:
        llm_fn = llm_groq
    else:
        llm_fn = llm_google

    userdata = {"job": ctx, "llm_fn": llm_fn}

    return AgentSession(
        stt=openai.STT(model="gpt-realtime"),
        tts=tts.ElevenLabsTTS(api_key=ELEVEN_KEY, voice="Rachel"),
        userdata=userdata,
    )
