"""Embeddings com modelo falso; índice FAISS e Retriever reais."""

import numpy as np
import pytest

from app.embeddings import EmbeddingService
from app.models import Chunk
from app.retriever import Retriever
from app.vector_store import VectorStore


class FakeTokenizer:
    def encode(self, text, add_special_tokens, truncation):
        return [0, *range(len(text.split())), 1]


class FakeSentenceModel:
    max_seq_length = 5
    tokenizer = FakeTokenizer()

    def get_embedding_dimension(self):
        return 2

    def encode(self, texts, convert_to_numpy, show_progress_bar):
        mapping = {
            "alpha": [1.0, 0.0],
            "beta": [0.0, 1.0],
            "pergunta": [0.9, 0.1],
            "invalido": [float("nan"), 0.0],
        }
        return np.array([mapping[text] for text in texts], dtype=np.float32)


def chunk(identifier, page):
    return Chunk(identifier, identifier, "manual.pdf", page)


def test_embeddings_validate_count_dimension_values_and_truncation(monkeypatch):
    monkeypatch.setattr("app.embeddings.SentenceTransformer", lambda _: FakeSentenceModel())
    embeddings = EmbeddingService("modelo-falso")

    documents = embeddings.encode_documents(["alpha", "beta"])
    query = embeddings.encode_query("pergunta")

    assert embeddings.dimension == 2
    assert documents.shape == (2, 2)
    assert query.shape == (1, 2)
    assert np.isfinite(documents).all() and np.isfinite(query).all()
    assert embeddings.count_truncated(["um dois", "um dois tres quatro"]) == 1

    with pytest.raises(ValueError, match="não vazios"):
        embeddings.encode_documents(["alpha", "  "])
    with pytest.raises(ValueError, match="pergunta"):
        embeddings.encode_query(" ")
    with pytest.raises(ValueError, match="limite de tokens"):
        embeddings.encode_query("um dois tres quatro")
    with pytest.raises(RuntimeError, match="Embeddings inválidos"):
        embeddings.encode_documents(["invalido"])


def test_faiss_returns_normalized_top_k_with_correct_metadata():
    store = VectorStore()
    chunks = [chunk("alpha", 2), chunk("beta", 7)]
    store.build(chunks, np.array([[3.0, 0.0], [0.0, 2.0]], dtype=np.float32))

    results = store.search(np.array([[0.9, 0.1]], dtype=np.float32), top_k=10)

    assert [result.chunk.id for result in results] == ["alpha", "beta"]
    assert [(result.chunk.source, result.chunk.page) for result in results] == [
        ("manual.pdf", 2),
        ("manual.pdf", 7),
    ]
    assert results[0].score > results[1].score
    assert 0.9 < results[0].score <= 1.0  # Cosseno após normalização.
    assert len(store.search(np.array([[1.0, 0.0]], dtype=np.float32), 1)) == 1


def test_faiss_rejects_invalid_vectors_without_damaging_existing_index():
    store = VectorStore()
    with pytest.raises(RuntimeError, match="não foi construído"):
        store.search(np.array([[1.0, 0.0]], dtype=np.float32), 1)

    store.build([chunk("alpha", 2)], np.array([[1.0, 0.0]], dtype=np.float32))
    with pytest.raises(ValueError, match="NaN"):
        store.build([chunk("beta", 7)], np.array([[np.nan, 0.0]], dtype=np.float32))
    with pytest.raises(ValueError, match="norma zero"):
        store.search(np.array([[0.0, 0.0]], dtype=np.float32), 1)

    assert store.search(np.array([[1.0, 0.0]], dtype=np.float32), 1)[0].chunk.id == "alpha"


def test_retriever_embeds_question_and_returns_top_k_without_llm():
    class QueryEmbeddings:
        questions = []

        def encode_query(self, question):
            self.questions.append(question)
            return np.array([[1.0, 0.0]], dtype=np.float32)

    embeddings = QueryEmbeddings()
    store = VectorStore()
    store.build([chunk("alpha", 2), chunk("beta", 7)], np.eye(2, dtype=np.float32))

    result = Retriever(embeddings, store, top_k=1).retrieve("Pergunta de teste")

    assert embeddings.questions == ["Pergunta de teste"]
    assert len(result) == 1
    assert (result[0].chunk.id, result[0].chunk.page) == ("alpha", 2)
    assert result[0].score == pytest.approx(1.0)
