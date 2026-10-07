"""Composição do contexto rastreável enviado ao modelo generativo."""

from pathlib import Path

from app.models import RetrievedChunk


TEMPLATE = (Path(__file__).resolve().parents[1] / "prompts" / "rag_answer.txt").read_text(encoding="utf-8")


def build_prompt(
    question: str, results: list[RetrievedChunk], max_context_chars: int
) -> tuple[str, tuple[RetrievedChunk, ...]]:
    if not question.strip() or max_context_chars < 1:
        raise ValueError("Pergunta e limite de contexto devem ser válidos.")
    blocks: list[str] = []
    used: list[RetrievedChunk] = []
    length = 0
    for result in results:
        chunk = result.chunk
        block = f"[{chunk.source}, p. {chunk.page}]\n{chunk.text}"
        addition = len(block) + (2 if blocks else 0)
        if length + addition > max_context_chars:
            continue
        blocks.append(block)
        used.append(result)
        length += addition
    context = "\n\n".join(blocks) if blocks else "(nenhum trecho disponível)"
    prompt = TEMPLATE.format(context=context, question=question.strip())
    return prompt, tuple(used)
