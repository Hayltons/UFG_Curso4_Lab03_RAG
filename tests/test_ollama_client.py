"""Contrato HTTP do cliente Ollama sem serviço local."""

import io
import json
from urllib.error import HTTPError, URLError

import pytest

from app.ollama_client import OllamaClient


def test_client_sends_configured_model_and_returns_text(monkeypatch):
    sent = {}

    def fake_urlopen(request, timeout):
        sent.update(url=request.full_url, timeout=timeout, body=json.loads(request.data))
        return io.BytesIO(b'{"response":"  Resposta do manual.  "}')

    monkeypatch.setattr("app.ollama_client.urlopen", fake_urlopen)
    answer = OllamaClient("http://127.0.0.1:11434", "gemma3:4b", 12).generate("Prompt")

    assert answer == "Resposta do manual."
    assert sent == {
        "url": "http://127.0.0.1:11434/api/generate",
        "timeout": 12,
        "body": {"model": "gemma3:4b", "prompt": "Prompt", "stream": False},
    }


@pytest.mark.parametrize(
    "failure,message",
    [
        (HTTPError("http://127.0.0.1", 404, "Not Found", None, io.BytesIO(b"{}")), "Modelo Ollama"),
        (URLError("connection refused"), "Ollama indisponível"),
    ],
)
def test_client_explains_service_or_model_unavailable(monkeypatch, failure, message):
    def fake_urlopen(request, timeout):
        raise failure

    monkeypatch.setattr("app.ollama_client.urlopen", fake_urlopen)
    with pytest.raises(RuntimeError, match=message):
        OllamaClient("http://127.0.0.1:11434", "gemma3:4b", 12).generate("Prompt")


def test_client_rejects_empty_response(monkeypatch):
    monkeypatch.setattr("app.ollama_client.urlopen", lambda request, timeout: io.BytesIO(b'{"response":" "}'))
    with pytest.raises(RuntimeError, match="resposta vazia"):
        OllamaClient("http://127.0.0.1:11434", "gemma3:4b", 12).generate("Prompt")
