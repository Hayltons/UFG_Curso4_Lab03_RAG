"""Verificação manual repetível do backend com perguntas dentro e fora do PDF."""

from app.prompt_builder import build_prompt
from app.rag_service import create_service


QUESTIONS = (
    "Segundo o manual, como diagnosticar uma resposta incorreta em um sistema RAG?",
    "Qual é o preço atual do Bitcoin em reais?",
)


def main() -> None:
    service = create_service()
    report = service.ingest()
    print(f"Ingestão: {report.pages} páginas, {report.chunks} chunks, "
          f"dimensão {report.dimension}, truncados {report.truncated_chunks}")

    for question in QUESTIONS:
        print(f"\nPergunta: {question}")
        try:
            results = service.retriever.retrieve(question)
        except Exception as exc:
            raise RuntimeError(f"Falha de retrieval para {question!r}") from exc
        for result in results:
            chunk = result.chunk
            print(f"  Recuperado: {chunk.id} | score={result.score:.3f} | "
                  f"{chunk.source}, p. {chunk.page} | {chunk.text!r}")
        try:
            _, used = build_prompt(question, results, service.config.max_context_chars)
        except Exception as exc:
            raise RuntimeError(f"Falha de construção do contexto para {question!r}") from exc
        print(f"  Contexto enviado: {len(used)} chunks")
        try:
            answer = service.ask(question)
        except Exception as exc:
            raise RuntimeError(f"Falha na consulta integrada para {question!r}") from exc
        print(f"  Resposta: {answer.answer}")
        print(f"  Fontes consultadas: {[(x.chunk.source, x.chunk.page) for x in answer.sources]}")


if __name__ == "__main__":
    main()
