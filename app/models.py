"""Dados trocados entre as etapas do pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True)
class PageText:
    text: str
    source: str
    page: int


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    source: str
    page: int


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class RAGAnswer:
    answer: str
    sources: tuple[RetrievedChunk, ...]


@dataclass(frozen=True)
class IngestionReport:
    pages: int
    chunks: int
    dimension: int
    truncated_chunks: int
