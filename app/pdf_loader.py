"""Extração de texto do único PDF local, mantendo número da página."""

from pathlib import Path

import pymupdf

from app.models import PageText


def load_pdf(path: Path) -> list[PageText]:
    if not path.is_file():
        raise FileNotFoundError(f"PDF não encontrado: {path}")
    try:
        with pymupdf.open(path) as document:
            if not document.is_pdf:
                raise ValueError(f"O arquivo não é um PDF: {path}")
            if document.needs_pass:
                raise ValueError(f"O PDF exige senha e não pode ser lido: {path}")
            pages = [
                PageText(text=page.get_text().strip(), source=path.name, page=number)
                for number, page in enumerate(document, start=1)
            ]
    except (pymupdf.FileDataError, pymupdf.EmptyFileError) as exc:
        raise ValueError(f"PDF inválido ou ilegível: {path}") from exc
    pages = [page for page in pages if page.text]
    if not pages:
        raise ValueError(f"O PDF não contém texto extraível: {path}")
    return pages
