import json
from typing import Generator

import requests


class OllamaClient:
    """HTTP client responsible only for communicating with Ollama."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "qwen2.5-coder:7b",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        stream: bool = False,
        timeout: int | float | None = None,
    ) -> str:
        """Generate a non-streaming response from Ollama."""

        url = f"{self.base_url}/api/generate"

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
        }

        response = requests.post(
            url,
            json=data,
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json().get("response", "").strip()

    def stream_generate(
        self,
        prompt: str,
        *,
        timeout: int | float | None = None,
    ) -> Generator[str, None, None]:
        """Yield response chunks from a streaming Ollama request."""

        url = f"{self.base_url}/api/generate"

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
        }

        response = requests.post(
            url,
            json=data,
            stream=True,
            timeout=timeout,
        )

        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line)

            text = chunk.get("response", "")

            if text:
                yield text

            if chunk.get("done", False):
                break