# utils/recorder.py
import asyncio
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from livekit import rtc


@dataclass
class RecorderConfig:
    sample_rate: int = 48000
    channels: int = 1          # mono
    sample_width: int = 2      # 16-bit


class RoomAudioRecorder:
    def __init__(self, room: rtc.Room, room_name: str, base_dir: Path):
        self._room = room
        self._room_name = room_name
        self._base_dir = base_dir
        self._cfg = RecorderConfig()
        self._wav_file: Optional[wave.Wave_write] = None
        self._tasks: list[asyncio.Task] = []
        self._closed = False

    def _ensure_dir(self) -> Path:
        self._base_dir.mkdir(parents=True, exist_ok=True)
        return self._base_dir / f"{self._room_name}.wav"

    async def _stream_to_wav(self, audio_stream: rtc.AudioStream):
        assert self._wav_file is not None
        async for frame in audio_stream:
            if self._closed:
                break
            # frame.data là PCM 16-bit (theo docs / ví dụ)
            self._wav_file.writeframes(frame.data)

    def start(self):
        """
        Đăng ký event track_subscribed để thu tất cả audio track
        (user + agent). Đơn giản: đổ chung vào 1 WAV.
        """
        if self._wav_file is not None:
            return

        out_path = self._ensure_dir()
        self._wav_file = wave.open(str(out_path), "wb")
        self._wav_file.setframerate(self._cfg.sample_rate)
        self._wav_file.setnchannels(self._cfg.channels)
        self._wav_file.setsampwidth(self._cfg.sample_width)

        @self._room.on("track_subscribed")
        def _on_track_subscribed(track: rtc.Track, publication, participant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                stream = rtc.AudioStream(track)
                task = asyncio.create_task(self._stream_to_wav(stream))
                self._tasks.append(task)

    async def stop(self):
        if self._closed:
            return
        self._closed = True
        # Đợi các task kết thúc
        for t in self._tasks:
            try:
                await t
            except Exception:
                pass
        self._tasks.clear()
        if self._wav_file is not None:
            self._wav_file.close()
            self._wav_file = None
