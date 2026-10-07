"""Contratos de extração por página e chunking sem modelo externo."""

import pymupdf
import pytest

from app.chunker import chunk_pages
from app.models import PageText
from app.pdf_loader import load_pdf


def test_loader_preserves_source_and_original_page_numbers(tmp_path):
    path = tmp_path / "manual.pdf"
    with pymupdf.open() as document:
        document.new_page().insert_text((72, 72), "Primeira pagina")
        document.new_page()  # A página sem texto não desloca a numeração seguinte.
        document.new_page().insert_text((72, 72), "Terceira pagina")
        document.save(path)

    pages = load_pdf(path)

    assert [(page.page, page.source) for page in pages] == [
        (1, "manual.pdf"),
        (3, "manual.pdf"),
    ]
    assert "Primeira pagina" in pages[0].text
    assert "Terceira pagina" in pages[1].text


def test_loader_reports_missing_invalid_and_textless_pdf(tmp_path):
    with pytest.raises(FileNotFoundError, match="PDF não encontrado"):
        load_pdf(tmp_path / "ausente.pdf")

    invalid = tmp_path / "invalido.pdf"
    invalid.write_bytes(b"isto nao e um pdf")
    with pytest.raises(ValueError, match="PDF inválido"):
        load_pdf(invalid)

    textless = tmp_path / "sem-texto.pdf"
    with pymupdf.open() as document:
        document.new_page()
        document.save(textless)
    with pytest.raises(ValueError, match="não contém texto"):
        load_pdf(textless)


def test_chunker_keeps_overlap_page_and_unique_ids():
    pages = [PageText("abcdefghij", "manual.pdf", 2), PageText("XYZ", "manual.pdf", 4)]

    chunks = chunk_pages(pages, chunk_size=6, chunk_overlap=2)

    assert [chunk.text for chunk in chunks] == ["abcdef", "efghij", "XYZ"]
    assert [(chunk.source, chunk.page) for chunk in chunks] == [
        ("manual.pdf", 2),
        ("manual.pdf", 2),
        ("manual.pdf", 4),
    ]
    assert [chunk.id for chunk in chunks] == [
        "manual.pdf:p2:c1",
        "manual.pdf:p2:c2",
        "manual.pdf:p4:c1",
    ]


@pytest.mark.parametrize("size,overlap", [(0, 0), (6, 6), (6, -1)])
def test_chunker_rejects_invalid_window(size, overlap):
    with pytest.raises(ValueError, match="CHUNK_SIZE"):
        chunk_pages([PageText("texto", "manual.pdf", 1)], size, overlap)
