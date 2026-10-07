"""Busca vetorial sem dependência do modelo generativo."""

from app.embeddings import EmbeddingService
from app.models import RetrievedChunk
from app.vector_store import VectorStore


class Retriever:
    def __init__(self, embeddings: EmbeddingService, store: VectorStore, top_k: int) -> None:
        self.embeddings = embeddings
        self.store = store
        self.top_k = top_k

    def retrieve(self, question: str) -> list[RetrievedChunk]:
        return self.store.search(self.embeddings.encode_query(question), self.top_k)
