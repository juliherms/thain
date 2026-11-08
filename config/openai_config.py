"""Configuração do provedor OpenAI (api.openai.com ou endpoint compatível)."""

from agent_framework.openai import OpenAIChatCompletionClient

from config.settings import OpenAISettings, optional, required


def load_openai_settings() -> OpenAISettings:
    return OpenAISettings(
        api_key=required("OPENAI_API_KEY"),
        model=required("OPENAI_MODEL"),
        base_url=optional("OPENAI_BASE_URL"),
    )


def create_openai_client(s: OpenAISettings) -> OpenAIChatCompletionClient:
    return OpenAIChatCompletionClient(
        model=s.model,
        api_key=s.api_key,
        base_url=s.base_url,
    )
