"""Índice FAISS exato em memória com mapeamento para trechos."""

import faiss
import numpy as np

from app.models import Chunk, RetrievedChunk


class VectorStore:
    def __init__(self) -> None:
        self._index: faiss.IndexFlatIP | None = None
        self._chunks: list[Chunk] = []

    @property
    def ready(self) -> bool:
        return self._index is not None

    def build(self, chunks: list[Chunk], vectors: np.ndarray) -> None:
        matrix = np.asarray(vectors, dtype=np.float32)
        if not chunks or matrix.ndim != 2 or matrix.shape[0] != len(chunks) or matrix.shape[1] < 1:
            raise ValueError("É necessário um vetor por trecho e uma dimensão positiva.")
        if not np.isfinite(matrix).all():
            raise ValueError("Os vetores não podem conter NaN ou infinito.")
        matrix = np.ascontiguousarray(matrix.copy())
        if np.any(np.linalg.norm(matrix, axis=1) == 0):
            raise ValueError("Os vetores não podem ter norma zero.")
        faiss.normalize_L2(matrix)
        index = faiss.IndexFlatIP(matrix.shape[1])
        index.add(matrix)
        self._index, self._chunks = index, list(chunks)

    def search(self, vector: np.ndarray, top_k: int) -> list[RetrievedChunk]:
        if self._index is None:
            raise RuntimeError("O índice ainda não foi construído.")
        if top_k < 1:
            raise ValueError("TOP_K deve ser positivo.")
        query = np.asarray(vector, dtype=np.float32)
        if query.shape != (1, self._index.d) or not np.isfinite(query).all():
            raise ValueError("O vetor da pergunta tem dimensão ou valores inválidos.")
        query = np.ascontiguousarray(query.copy())
        if np.linalg.norm(query) == 0:
            raise ValueError("O vetor da pergunta não pode ter norma zero.")
        faiss.normalize_L2(query)
        scores, indexes = self._index.search(query, min(top_k, len(self._chunks)))
        return [
            RetrievedChunk(chunk=self._chunks[int(index)], score=float(score))
            for score, index in zip(scores[0], indexes[0])
            if index >= 0
        ]
