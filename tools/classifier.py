"""
Classificador simples baseado em palavras-chave.
Representa uma Tool
"""


import re
import unicodedata

CATEGORIES: dict[str, tuple[str, ...]] = {
    "saudacao": ("oi", "ola", "bom dia", "boa tarde", "boa noite"),
    "suporte": ("erro", "problema", "falha", "bug", "nao funciona", "ajuda"),
    "financeiro": ("pagamento", "fatura", "boleto", "cobranca", "reembolso"),
    "duvida": ("como", "quando", "onde", "porque", "qual", "duvida"),
}
DEFAULT_CATEGORY = "geral"


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def classify(text: str) -> str:
    """Retorna a categoria com mais palavras-chave encontradas no texto."""
    normalized = _normalize(text)
    scores = {
        category: sum(
            1 for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", normalized)
        )
        for category, keywords in CATEGORIES.items()
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else DEFAULT_CATEGORY
