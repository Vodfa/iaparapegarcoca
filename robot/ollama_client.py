from dataclasses import dataclass
from typing import List

import requests


@dataclass
class Message:
    role: str
    content: str


class OllamaClient:
    def __init__(self, base_url: str, model: str, temperature: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._temperature = temperature

    def chat(self, messages: List[Message]) -> str:
        payload = {
            "model": self._model,
            "messages": [message.__dict__ for message in messages],
            "stream": False,
            "options": {"temperature": self._temperature},
        }
        response = requests.post(f"{self._base_url}/api/chat", json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
