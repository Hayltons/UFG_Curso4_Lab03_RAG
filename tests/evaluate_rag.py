"""Coleta observações reais para revisão manual de retrieval e grounding."""

import json
from pathlib import Path

from app.config import load_config
from app.prompt_builder import build_prompt
from app.rag_service import create_service


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "tests" / "eval_cases.jsonl"
OUTPUT = ROOT / "docs" / "avaliacao-rag-observacoes.jsonl"


def main() -> None:
    config = load_config()
    if config.ollama_model != "gemma3:4b":
        raise ValueError("A avaliação do CAP05 exige OLLAMA_MODEL=gemma3:4b.")
    expected_pdf = ROOT / "data" / "guia-pratico-engenharia-software-com-ia-generativa.pdf"
    if config.pdf_path.resolve() != expected_pdf.resolve():
        raise ValueError(f"A avaliação do CAP05 exige PDF_PATH={expected_pdf}.")
    if config.embedding_model != "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2":
        raise ValueError("A avaliação do CAP05 exige o modelo de embeddings baseline.")
    if (config.top_k, config.chunk_size, config.chunk_overlap, config.max_context_chars) != (4, 350, 50, 2500):
        raise ValueError(
            "A avaliação do CAP05 exige TOP_K=4, CHUNK_SIZE=350, "
            "CHUNK_OVERLAP=50 e MAX_CONTEXT_CHARS=2500."
        )

    service = create_service(config)
    report = service.ingest()
    cases = [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"Indexado: {report.pages} páginas, {report.chunks} chunks, dimensão {report.dimension}.")

    failures = 0
    with OUTPUT.open("w", encoding="utf-8") as output:
        for case in cases:
            observation = {"id": case["id"], "question": case["question"]}
            try:
                results = service.retriever.retrieve(case["question"])
                observation["retrieved"] = [
                    {
                        "id": item.chunk.id,
                        "page": item.chunk.page,
                        "score": round(item.score, 3),
                        "text": item.chunk.text,
                    }
                    for item in results
                ]
            except Exception as exc:
                observation["failure"] = {"stage": "retrieval", "error": str(exc)}

            if "failure" not in observation:
                try:
                    _, used = build_prompt(case["question"], results, config.max_context_chars)
                    observation["context_chunk_ids"] = [item.chunk.id for item in used]
                except Exception as exc:
                    observation["failure"] = {"stage": "contexto", "error": str(exc)}

            if "failure" not in observation:
                try:
                    answer = service.ask(case["question"])
                    observation["answer"] = answer.answer
                    observation["source_pages"] = [item.chunk.page for item in answer.sources]
                except Exception as exc:
                    observation["failure"] = {"stage": "consulta integrada/geração", "error": str(exc)}

            output.write(json.dumps(observation, ensure_ascii=False) + "\n")
            failures += "failure" in observation
            pages = [item["page"] for item in observation.get("retrieved", [])]
            print(f"{case['id']}: páginas Top-K={pages}; falha={observation.get('failure', 'nenhuma')}")

    print(f"Observações: {OUTPUT.relative_to(ROOT)}; falhas técnicas: {failures}.")
    if failures:
        raise RuntimeError("A avaliação encontrou falhas técnicas; consulte as observações.")


if __name__ == "__main__":
    main()
