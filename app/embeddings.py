"""Codificação de documentos e perguntas com o mesmo modelo."""

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str) -> None:
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as exc:
            raise RuntimeError(f"Não foi possível carregar o modelo de embeddings {model_name!r}.") from exc
        self.dimension = self.model.get_embedding_dimension()
        if not self.dimension:
            raise RuntimeError("O modelo de embeddings não informou sua dimensão.")

    def count_truncated(self, texts: list[str]) -> int:
        """Conta textos que excedem o limite de tokens do modelo antes da codificação."""
        limit = self.model.max_seq_length
        if limit is None:
            return 0
        return sum(
            len(self.model.tokenizer.encode(text, add_special_tokens=True, truncation=False)) > limit
            for text in texts
        )

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        if not texts or any(not text.strip() for text in texts):
            raise ValueError("Documentos para embeddings devem conter textos não vazios.")
        vectors = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return self._validate(vectors, len(texts))

    def encode_query(self, question: str) -> np.ndarray:
        if not question.strip():
            raise ValueError("A pergunta não pode estar vazia.")
        if self.count_truncated([question]):
            raise ValueError("A pergunta excede o limite de tokens do modelo de embeddings.")
        vector = self.model.encode([question], convert_to_numpy=True, show_progress_bar=False)
        return self._validate(vector, 1)

    def _validate(self, vectors: np.ndarray, count: int) -> np.ndarray:
        result = np.asarray(vectors, dtype=np.float32)
        if result.shape != (count, self.dimension) or not np.isfinite(result).all():
            raise RuntimeError("Embeddings inválidos: quantidade, dimensão ou valores incorretos.")
        return result
