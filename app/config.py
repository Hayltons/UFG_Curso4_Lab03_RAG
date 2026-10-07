"""Configuração local validada do backend."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Config:
    pdf_path: Path
    embedding_model: str
    ollama_model: str
    ollama_url: str
    top_k: int
    chunk_size: int
    chunk_overlap: int
    max_context_chars: int
    ollama_timeout: int

    def __post_init__(self) -> None:
        if not self.embedding_model.strip() or not self.ollama_model.strip():
            raise ValueError("Os nomes dos modelos de embeddings e Ollama são obrigatórios.")
        if not self.ollama_url.startswith(("http://", "https://")):
            raise ValueError("OLLAMA_URL deve começar com http:// ou https://.")
        if self.top_k < 1 or self.chunk_size < 1 or self.max_context_chars < 1:
            raise ValueError("TOP_K, CHUNK_SIZE e MAX_CONTEXT_CHARS devem ser positivos.")
        if not 0 <= self.chunk_overlap < self.chunk_size:
            raise ValueError("CHUNK_OVERLAP deve estar entre zero e CHUNK_SIZE - 1.")
        if self.ollama_timeout < 1:
            raise ValueError("OLLAMA_TIMEOUT deve ser positivo.")


def load_config() -> Config:
    """Lê .env do projeto; variáveis já definidas no ambiente prevalecem."""
    load_dotenv(PROJECT_ROOT / ".env", override=False)

    def positive_int(name: str, default: int) -> int:
        raw = os.getenv(name, str(default))
        try:
            return int(raw)
        except ValueError as exc:
            raise ValueError(f"{name} deve ser um número inteiro: {raw!r}.") from exc

    pdf_path = Path(os.getenv("PDF_PATH", "data/guia-pratico-engenharia-software-com-ia-generativa.pdf"))
    if not pdf_path.is_absolute():
        pdf_path = PROJECT_ROOT / pdf_path
    return Config(
        pdf_path=pdf_path,
        embedding_model=os.getenv(
            "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        ),
        ollama_model=os.getenv("OLLAMA_MODEL", "gemma3:4b"),
        ollama_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
        top_k=positive_int("TOP_K", 4),
        chunk_size=positive_int("CHUNK_SIZE", 350),
        chunk_overlap=positive_int("CHUNK_OVERLAP", 50),
        max_context_chars=positive_int("MAX_CONTEXT_CHARS", 2500),
        ollama_timeout=positive_int("OLLAMA_TIMEOUT", 120),
    )
