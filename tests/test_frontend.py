"""Interações da UI com um serviço falso, sem Ollama ou modelo externo."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.models import Chunk, RAGAnswer, RetrievedChunk


APP_PATH = Path(__file__).resolve().parents[1] / "streamlit_app.py"


class FakeService:
    def __init__(self, config):
        self.config = config
        self.ingestions = 0
        self.questions = []
        self.error = None

    def ingest(self):
        self.ingestions += 1

    def ask(self, question):
        self.questions.append(question)
        if self.error:
            raise self.error
        source = RetrievedChunk(Chunk("p3", "Evidência", "manual.pdf", 3), 0.9)
        return RAGAnswer("Resposta de teste.", (source, source))


def test_form_reuses_service_validates_input_and_displays_sources(monkeypatch):
    created = []

    def fake_factory(config):
        service = FakeService(config)
        created.append(service)
        return service

    monkeypatch.setattr("app.rag_service.create_service", fake_factory)
    app = AppTest.from_file(APP_PATH, default_timeout=60).run()

    assert not app.exception and len(created) == 1
    assert created[0].ingestions == 1
    assert len(app.text_input) == 1 and len(app.button) == 1

    app.button[0].click().run()
    assert "Digite uma pergunta" in app.warning[0].value
    assert created[0].questions == []
    assert app.session_state["rag_service"] is created[0]

    app.text_input[0].set_value("  O que diz o manual?  ")
    app.button[0].click().run()
    assert created[0].questions == ["O que diz o manual?"]
    assert created[0].ingestions == 1
    assert app.session_state["last_answer"].answer == "Resposta de teste."
    assert sum("manual.pdf — página 3" in item.value for item in app.markdown) == 1
    assert not app.exception

    created[0].error = RuntimeError("Ollama indisponível")
    app.button[0].click().run()
    assert "Ollama indisponível" in app.error[0].value
    assert "last_answer" not in app.session_state
    assert not app.exception

    monkeypatch.setenv("TOP_K", "3")
    app.run()
    assert len(created) == 2 and created[1].config.top_k == 3
    assert created[1].ingestions == 1


def test_missing_pdf_is_shown_without_traceback(monkeypatch, tmp_path):
    monkeypatch.setenv("PDF_PATH", str(tmp_path / "ausente.pdf"))
    app = AppTest.from_file(APP_PATH, default_timeout=60).run()

    assert "PDF não encontrado" in app.error[0].value
    assert not app.exception
    assert len(app.text_input) == 0
