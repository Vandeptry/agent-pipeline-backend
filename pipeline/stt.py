# pipeline/stt.py
from livekit.plugins import deepgram


def build_stt() -> deepgram.STT:
    # Deepgram model nova-3 là bản phổ biến cho hội thoại  :contentReference[oaicite:2]{index=2}
    return deepgram.STT(model="nova-3")
