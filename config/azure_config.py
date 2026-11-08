"""Configuração do provedor Azure OpenAI (chave de API ou Entra ID)."""

from agent_framework.openai import OpenAIChatCompletionClient

from config.settings import AzureSettings, optional, required


def load_azure_settings() -> AzureSettings:
    import os

    return AzureSettings(
        endpoint=required("AZURE_OPENAI_ENDPOINT"),
        deployment=required("AZURE_OPENAI_DEPLOYMENT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        api_key=optional("AZURE_OPENAI_API_KEY"),
    )


def create_azure_client(s: AzureSettings) -> OpenAIChatCompletionClient:
    if s.api_key:
        return OpenAIChatCompletionClient(
            model=s.deployment,
            azure_endpoint=s.endpoint,
            api_version=s.api_version,
            api_key=s.api_key,
        )

    # Sem chave: usa Entra ID (az login, variáveis de ambiente, managed identity...)
    from azure.identity import DefaultAzureCredential

    return OpenAIChatCompletionClient(
        model=s.deployment,
        azure_endpoint=s.endpoint,
        api_version=s.api_version,
        credential=DefaultAzureCredential(),
    )
