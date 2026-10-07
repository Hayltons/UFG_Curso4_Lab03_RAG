"""Orquestração explícita dos fluxos de ingestão e consulta."""

from app.chunker import chunk_pages
from app.config import Config, load_config
from app.embeddings import EmbeddingService
from app.models import IngestionReport, RAGAnswer
from app.ollama_client import OllamaClient
from app.pdf_loader import load_pdf
from app.prompt_builder import build_prompt
from app.retriever import Retriever
from app.vector_store import VectorStore


class RAGService:
    def __init__(self, config: Config, embeddings: EmbeddingService) -> None:
        self.config = config
        self.embeddings = embeddings
        self.store = VectorStore()
        self.retriever = Retriever(embeddings, self.store, config.top_k)
        self.llm = OllamaClient(config.ollama_url, config.ollama_model, config.ollama_timeout)

    def ingest(self) -> IngestionReport:
        pages = load_pdf(self.config.pdf_path)
        chunks = chunk_pages(pages, self.config.chunk_size, self.config.chunk_overlap)
        if not chunks:
            raise ValueError("O PDF não produziu trechos indexáveis.")
        truncated = self.embeddings.count_truncated([chunk.text for chunk in chunks])
        if truncated:
            raise ValueError(
                f"{truncated} trechos excedem o limite de tokens do modelo de embeddings; "
                "reduza CHUNK_SIZE para evitar perda silenciosa de texto."
            )
        vectors = self.embeddings.encode_documents([chunk.text for chunk in chunks])
        self.store.build(chunks, vectors)
        return IngestionReport(len(pages), len(chunks), self.embeddings.dimension, truncated)

    def ask(self, question: str) -> RAGAnswer:
        if not question.strip():
            raise ValueError("A pergunta não pode estar vazia.")
        if not self.store.ready:
            raise RuntimeError("Execute ingest() antes de ask().")
        results = self.retriever.retrieve(question)
        prompt, used = build_prompt(question, results, self.config.max_context_chars)
        if not used:
            return RAGAnswer("Não encontrei essa informação no manual consultado.", ())
        return RAGAnswer(self.llm.generate(prompt), used)


def create_service(config: Config | None = None) -> RAGService:
    chosen = config or load_config()
    return RAGService(chosen, EmbeddingService(chosen.embedding_model))
