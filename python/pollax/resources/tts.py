"""TTS / broadcast preview resource"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import Pollax


class TtsResource:
    """Text-to-speech preview API resource"""

    def __init__(self, client: "Pollax"):
        self._client = client

    def broadcast_preview(
        self,
        text: str,
        language: Optional[str] = None,
        speed: Optional[float] = None,
        resolved: Optional[bool] = None,
    ) -> dict:
        """Preview one-way broadcast TTS audio."""
        data = {"text": text}
        if language is not None:
            data["language"] = language
        if speed is not None:
            data["speed"] = speed
        if resolved is not None:
            data["resolved"] = resolved
        return self._client.request("POST", "/api/v1/tts/broadcast-preview", json=data)
