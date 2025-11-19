# pipeline/tts.py
from livekit.plugins import elevenlabs


def build_tts() -> elevenlabs.TTS:
    return elevenlabs.TTS()
