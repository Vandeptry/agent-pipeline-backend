# pipeline/llm.py
from livekit.plugins import openai


def build_llm() -> openai.LLM:
    return openai.LLM(model="gpt-4o-mini")
