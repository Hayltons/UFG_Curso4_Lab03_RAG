"""Divisão por página em janelas de caracteres sobrepostas."""

from app.models import Chunk, PageText


def chunk_pages(pages: list[PageText], chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    if chunk_size < 1 or not 0 <= chunk_overlap < chunk_size:
        raise ValueError("Use CHUNK_SIZE positivo e 0 <= CHUNK_OVERLAP < CHUNK_SIZE.")
    chunks: list[Chunk] = []
    stride = chunk_size - chunk_overlap
    for page in pages:
        text = page.text.strip()
        for start in range(0, len(text), stride):
            part = text[start : start + chunk_size].strip()
            if part:
                chunks.append(
                    Chunk(
                        id=f"{page.source}:p{page.page}:c{start // stride + 1}",
                        text=part,
                        source=page.source,
                        page=page.page,
                    )
                )
            if start + chunk_size >= len(text):
                break
    return chunks
