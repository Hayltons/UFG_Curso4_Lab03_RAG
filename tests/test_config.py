"""Leitura e validação de configuração sem alterar o .env do usuário."""

import pytest

import app.config as config_module


@pytest.fixture
def isolated_config(monkeypatch, tmp_path):
    monkeypatch.setattr(config_module, "PROJECT_ROOT", tmp_path)
    for name in (
        "PDF_PATH", "EMBEDDING_MODEL", "OLLAMA_MODEL", "OLLAMA_URL", "TOP_K",
        "CHUNK_SIZE", "CHUNK_OVERLAP", "MAX_CONTEXT_CHARS", "OLLAMA_TIMEOUT",
    ):
        monkeypatch.delenv(name, raising=False)
    return tmp_path


def test_defaults_keep_embedding_and_generative_models_separate(isolated_config):
    config = config_module.load_config()

    assert config.pdf_path == isolated_config / "data/guia-pratico-engenharia-software-com-ia-generativa.pdf"
    assert config.embedding_model == "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    assert config.ollama_model == "gemma3:4b"
    assert (config.top_k, config.chunk_size, config.chunk_overlap) == (4, 350, 50)


def test_dotenv_is_reread_and_process_environment_has_precedence(isolated_config, monkeypatch):
    env_file = isolated_config / ".env"
    env_file.write_text("TOP_K=3\nOLLAMA_MODEL=outro:1\n", encoding="utf-8")
    assert config_module.load_config().top_k == 3

    env_file.write_text("TOP_K=5\nOLLAMA_MODEL=outro:1\n", encoding="utf-8")
    assert config_module.load_config().top_k == 5
    monkeypatch.setenv("TOP_K", "2")
    assert config_module.load_config().top_k == 2
    assert config_module.load_config().ollama_model == "outro:1"


@pytest.mark.parametrize(
    "name,value,message",
    [
        ("TOP_K", "zero", "número inteiro"),
        ("TOP_K", "0", "positivos"),
        ("CHUNK_OVERLAP", "350", "CHUNK_OVERLAP"),
        ("OLLAMA_MODEL", " ", "obrigatórios"),
        ("OLLAMA_URL", "localhost:11434", "OLLAMA_URL"),
    ],
)
def test_invalid_configuration_is_rejected(isolated_config, monkeypatch, name, value, message):
    monkeypatch.setenv(name, value)
    with pytest.raises(ValueError, match=message):
        config_module.load_config()
