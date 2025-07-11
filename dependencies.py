from typing import cast

from services import LLMService, OllamaLLMService, StubbedLLMService
from settings import OllamaLLMServiceSettings, settings


def get_llm_service() -> LLMService:
    if settings.llm_service.type == 'ollama':
        settings.llm_service = cast(OllamaLLMServiceSettings, settings.llm_service)
        return OllamaLLMService(
            base_url=settings.llm_service.base_url,
            model=settings.llm_service.model,
        )
    return StubbedLLMService()
