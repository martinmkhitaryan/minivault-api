from enum import Enum
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class LLMServiceSettings(BaseSettings):
    pass


class StubbedLLMServiceSettings(LLMServiceSettings):
    type: Literal["stubbed"] = "stubbed"


class OllamaLLMServiceSettings(LLMServiceSettings):
    type: Literal["ollama"] = "ollama"
    model: str = "tinyllama"
    base_url: str = "http://localhost:11434"


class Settings(BaseSettings):
    llm_service: StubbedLLMServiceSettings | OllamaLLMServiceSettings = Field(
        default=StubbedLLMServiceSettings(), discriminator='type'
    )

    class Config:
        env_prefix = "MINIVAULT_"
        env_nested_delimiter = "__"


settings = Settings()
print(settings)
