"""Thain: ponto de entrada que coordena configuração, ferramentas e memória."""

import asyncio

from agent_framework import Agent, Message

from config.client import create_chat_client
from config.settings import load_settings
from memory.buffer import MemoryBuffer
from tools.classifier import classify

INSTRUCTIONS = "Você é o Thain, um assistente prestativo e objetivo. Responda em português."


async def main() -> None:
    settings = load_settings()
    agent = Agent(client=create_chat_client(settings), instructions=INSTRUCTIONS, name="Thain")
    memory = MemoryBuffer(settings.memory_size)

    print(f"Thain pronto (provedor: {settings.provider}).")
    print("Digite 'sair' para encerrar, 'limpar' para zerar a memória.")
    while True:
        try:
            user_input = (await asyncio.to_thread(input, "\nVocê: ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in {"sair", "exit", "quit"}:
            break
        if user_input.lower() == "limpar":
            memory.clear()
            print("Thain: memória limpa.")
            continue

        category = classify(user_input)
        memory.add("user", f"[categoria: {category}] {user_input}")

        try:
            history = [Message(m["role"], [m["content"]]) for m in memory.get()]
            response = await agent.run(history)
        except Exception as exc:  # erro de rede/credencial não deve derrubar o loop
            print(f"Thain: erro ao chamar o modelo: {exc}")
            continue

        answer = response.text or ""
        memory.add("assistant", answer)
        print(f"[{category}] Thain: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
