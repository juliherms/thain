"""Fábrica do cliente de chat conforme o provedor configurado."""

from config.settings import PROVIDER_AZURE, Settings


def create_chat_client(settings: Settings):
    if settings.provider == PROVIDER_AZURE:
        from config.azure_config import create_azure_client

        return create_azure_client(settings.azure)

    from config.openai_config import create_openai_client

    return create_openai_client(settings.openai)
