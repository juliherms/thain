# Thain

Agente de linha de comando construído com o Microsoft Agent Framework. Roda com **OpenAI** ou **Azure OpenAI** (escolha via `.env`), com um classificador por palavras-chave e um buffer de memória de curto prazo.

## Estrutura

```
thain/
  main.py                  # coordena configuração, ferramentas, memória e o loop do agente
  config/
    settings.py            # leitura do .env, seleção do provedor, dataclasses de config
    openai_config.py       # config e cliente OpenAI
    azure_config.py        # config e cliente Azure OpenAI (chave ou Entra ID)
    client.py              # fábrica: devolve o cliente conforme LLM_PROVIDER
  tools/classifier.py      # classificador simples por palavras-chave
  memory/buffer.py         # buffer em memória (últimas N mensagens)
  .env                     # variáveis de ambiente locais (não versionado)
  requirements.txt         # dependências
```

## Instalação

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Linux/macOS: `source .venv/bin/activate`.

## Configuração (.env)

Defina `LLM_PROVIDER` como `openai` ou `azure` e preencha só o bloco correspondente.

| Variável | Provedor | Descrição |
|---|---|---|
| `LLM_PROVIDER` | ambos | `openai` (padrão) ou `azure` |
| `OPENAI_API_KEY` | openai | Chave de API |
| `OPENAI_MODEL` | openai | Modelo, ex.: `gpt-4o-mini` |
| `OPENAI_BASE_URL` | openai | Opcional: endpoint compatível com OpenAI |
| `AZURE_OPENAI_ENDPOINT` | azure | URL do recurso |
| `AZURE_OPENAI_DEPLOYMENT` | azure | Nome do deployment |
| `AZURE_OPENAI_API_VERSION` | azure | Padrão `2024-10-21` |
| `AZURE_OPENAI_API_KEY` | azure | Opcional: se vazio, usa Entra ID (`az login`) |
| `MEMORY_SIZE` | ambos | Mensagens mantidas na memória (padrão `10`) |

## Execução

```powershell
python main.py
```

Comandos no chat: `sair` encerra, `limpar` zera a memória.

## Estendendo

- Novas categorias: edite `CATEGORIES` em `tools/classifier.py`.
- Novas ferramentas: adicione módulos em `tools/` e passe-as em `Agent(tools=[...])` no `main.py`.
- Novo provedor: crie `config/<nome>_config.py` e registre-o em `settings.py` e `client.py`.
