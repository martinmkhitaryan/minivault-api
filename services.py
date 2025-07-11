import abc
import asyncio
import random
from enum import Enum
from typing import Any, AsyncGenerator

import httpx
import orjson

GenerationMetadata = dict[str, Any]


class LLMService(abc.ABC):
    class Type(str, Enum):
        stubbed = "stubbed"
        ollama = "ollama"

    @abc.abstractmethod
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        raise NotImplementedError

    @staticmethod
    def get_type() -> Type:
        raise NotImplementedError


class StubbedLLMService(LLMService):
    def __init__(self):
        self.responses = [
            "Hello friend. Hello friend? That's lame. Maybe I should give you a name? But that's a slippery slope. You're only in my head. We have to remember that. Shit. It's actually happened. I'm talking to an imaginary person.",  # noqa
            "What if changing the world was just about being here, by showing up no matter how many times we get told we don't belong, by staying true even when we're shamed into being false, by believing in ourselves even when we're told we're too different? And if we all held on to that, if we refuse to budge and fall in line, if we stood our ground for long enough, just maybe… The world can't help but change around us.",  # noqa
        ]

    async def generate(self, prompt: str) -> str:
        return random.choice(self.responses)

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async def stream_generator():
            for chunk in random.choice(self.responses).split():
                yield f"{chunk} "
                await asyncio.sleep(0.01 * len(chunk))

        return stream_generator()

    @staticmethod
    def get_type() -> LLMService.Type:
        return LLMService.Type.stubbed


class OllamaLLMService(LLMService):
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "tinyllama"):
        self._base_url = base_url
        self._generate_url = f"{self._base_url}/api/generate"

        self._model = model
        self._client = httpx.AsyncClient(timeout=120)

    async def generate(self, prompt: str) -> str:
        response = await self._client.post(
            self._generate_url,
            json={"model": self._model, "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()['response']

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        async def stream_generator():
            async with self._client.stream(
                "POST",
                self._generate_url,
                json={"model": self._model, "prompt": prompt, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        data = orjson.loads(line)
                        yield data['response']

        return stream_generator()

    async def aclose(self):
        await self._client.aclose()

    @staticmethod
    def get_type() -> LLMService.Type:
        return LLMService.Type.ollama
