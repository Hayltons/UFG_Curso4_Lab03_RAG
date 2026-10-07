"""Orquestração do RAG sem PDF, embeddings ou Ollama externos."""

from dataclasses import replace

import numpy as np
import pytest

from app.config import Config
from app.models import Chunk, PageText, RetrievedChunk
from app.prompt_builder import build_prompt
from app.rag_service import RAGService


class FakeEmbeddings:
    dimension = 2

    def __init__(self, truncated=0):
        self.truncated = truncated
        self.document_calls = 0
        self.query_calls = 0

    def count_truncated(self, texts):
        return self.truncated

    def encode_documents(self, texts):
        self.document_calls += 1
        return np.tile(np.array([[1.0, 0.0]], dtype=np.float32), (len(texts), 1))

    def encode_query(self, question):
        self.query_calls += 1
        return np.array([[1.0, 0.0]], dtype=np.float32)


class FakeLLM:
    def __init__(self, error=None):
        self.prompts = []
        self.error = error

    def generate(self, prompt):
        self.prompts.append(prompt)
        if self.error:
            raise self.error
        return "Resposta fundamentada."


@pytest.fixture
def config(tmp_path):
    return Config(
        pdf_path=tmp_path / "manual.pdf",
        embedding_model="modelo-falso",
        ollama_model="gemma3:4b",
        ollama_url="http://127.0.0.1:11434",
        top_k=2,
        chunk_size=100,
        chunk_overlap=10,
        max_context_chars=500,
        ollama_timeout=10,
    )


@pytest.fixture
def fake_pdf(monkeypatch):
    monkeypatch.setattr(
        "app.rag_service.load_pdf",
        lambda _: [PageText("Evidência do manual para responder.", "manual.pdf", 3)],
    )


def test_prompt_includes_question_context_reference_and_only_used_sources():
    first = RetrievedChunk(Chunk("a", "evidencia breve", "manual.pdf", 3), 0.8)
    second = RetrievedChunk(Chunk("b", "outro trecho", "manual.pdf", 8), 0.6)
    first_block = "[manual.pdf, p. 3]\nevidencia breve"

    prompt, used = build_prompt("O que diz?", [first, second], len(first_block))

    assert used == (first,)
    assert "O que diz?" in prompt and first_block in prompt
    assert "[manual.pdf, p. 8]" not in prompt
    assert "Use somente o CONTEXTO" in prompt
    assert "Não invente fatos" in prompt

    _, empty = build_prompt("O que diz?", [first], 1)
    assert empty == ()
    with pytest.raises(ValueError, match="Pergunta"):
        build_prompt(" ", [first], 500)


def test_service_separates_ingestion_from_question_and_preserves_sources(config, fake_pdf):
    embeddings = FakeEmbeddings()
    llm = FakeLLM()
    service = RAGService(config, embeddings)
    service.llm = llm

    with pytest.raises(ValueError, match="pergunta"):
        service.ask("  ")
    with pytest.raises(RuntimeError, match="ingest"):
        service.ask("Pergunta válida")
    assert embeddings.query_calls == 0 and llm.prompts == []

    report = service.ingest()
    answer = service.ask("O que diz o manual?")

    assert (report.pages, report.chunks, report.dimension, report.truncated_chunks) == (1, 1, 2, 0)
    assert embeddings.document_calls == 1 and embeddings.query_calls == 1
    assert answer.answer == "Resposta fundamentada."
    assert [(source.chunk.source, source.chunk.page) for source in answer.sources] == [("manual.pdf", 3)]
    assert "O que diz o manual?" in llm.prompts[0]
    assert "[manual.pdf, p. 3]" in llm.prompts[0]


def test_service_abstains_without_usable_context_and_skips_llm(config, fake_pdf):
    llm = FakeLLM()
    service = RAGService(replace(config, max_context_chars=1), FakeEmbeddings())
    service.llm = llm
    service.ingest()

    answer = service.ask("Pergunta fora do contexto")

    assert "Não encontrei" in answer.answer
    assert answer.sources == ()
    assert llm.prompts == []


def test_service_reports_truncation_and_llm_failure(config, fake_pdf):
    truncated = RAGService(config, FakeEmbeddings(truncated=1))
    with pytest.raises(ValueError, match="excedem o limite"):
        truncated.ingest()
    assert not truncated.store.ready

    service = RAGService(config, FakeEmbeddings())
    service.llm = FakeLLM(error=RuntimeError("Ollama indisponível"))
    service.ingest()
    with pytest.raises(RuntimeError, match="Ollama indisponível"):
        service.ask("Pergunta válida")
