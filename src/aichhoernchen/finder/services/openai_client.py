from __future__ import annotations

from functools import lru_cache
from typing import Optional

from django.conf import settings
from openai import AzureOpenAI


class OpenAIConfigurationError(RuntimeError):
    """Raised when the Azure OpenAI client is misconfigured."""


def _require_setting(name: str) -> str:
    value: Optional[str] = getattr(settings, name, None)
    if not value:
        raise OpenAIConfigurationError(f"Missing Azure OpenAI setting: {name}")
    return value


@lru_cache(maxsize=1)
def get_azure_client() -> "AzureOpenAI":
    endpoint = _require_setting("AZURE_OPENAI_ENDPOINT")
    api_key = _require_setting("AZURE_OPENAI_API_KEY")
    api_version = getattr(settings, "AZURE_OPENAI_API_VERSION", None) or "2024-02-01"

    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )


def get_default_deployment() -> str:
    deployment = getattr(settings, "AZURE_OPENAI_IMAGE_ANALYSIS_DEPLOYMENT", None) or getattr(
        settings, "AZURE_OPENAI_DEPLOYMENT", None
    )
    if not deployment:
        raise OpenAIConfigurationError("No Azure OpenAI deployment configured")
    return deployment


__all__ = [
    "get_azure_client",
    "get_default_deployment",
    "OpenAIConfigurationError",
]
