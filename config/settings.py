"""Configurações de ambiente: seleção do provedor (OpenAI ou Azure OpenAI)."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

PROVIDER_OPENAI = "openai"
PROVIDER_AZURE = "azure"
PROVIDERS = (PROVIDER_OPENAI, PROVIDER_AZURE)


@dataclass(frozen=True)
class OpenAISettings:
    api_key: str
    model: str
    base_url: str | None = None


@dataclass(frozen=True)
class AzureSettings:
    endpoint: str
    deployment: str
    api_version: str
    api_key: str | None = None  # None => autenticação via Entra ID (azure-identity)


@dataclass(frozen=True)
class Settings:
    provider: str
    memory_size: int
    openai: OpenAISettings | None = None
    azure: AzureSettings | None = None


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.startswith("<"):
        raise RuntimeError(
            f"Variável de ambiente '{name}' não configurada. Edite o arquivo .env."
        )
    return value


def optional(name: str) -> str | None:
    value = os.getenv(name, "").strip()
    return None if not value or value.startswith("<") else value


def load_settings() -> Settings:
    load_dotenv(ENV_PATH)

    provider = os.getenv("LLM_PROVIDER", PROVIDER_OPENAI).strip().lower()
    if provider not in PROVIDERS:
        raise RuntimeError(
            f"LLM_PROVIDER inválido: '{provider}'. Use um de: {', '.join(PROVIDERS)}."
        )

    memory_size = int(os.getenv("MEMORY_SIZE", "10"))

    if provider == PROVIDER_OPENAI:
        from config.openai_config import load_openai_settings

        return Settings(provider, memory_size, openai=load_openai_settings())

    from config.azure_config import load_azure_settings

    return Settings(provider, memory_size, azure=load_azure_settings())
