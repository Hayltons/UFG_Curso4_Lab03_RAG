"""Cliente HTTP mínimo para a API de geração do Ollama."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class OllamaClient:
    def __init__(self, url: str, model: str, timeout: int) -> None:
        self.url = url
        self.model = model
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        request = Request(
            f"{self.url}/api/generate",
            data=json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = json.load(response)
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 404:
                raise RuntimeError(f"Modelo Ollama {self.model!r} indisponível. Verifique 'ollama list'.") from exc
            raise RuntimeError(f"Ollama retornou HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Ollama indisponível em {self.url}. Verifique se o serviço está ativo.") from exc
        except TimeoutError as exc:
            raise RuntimeError(f"Ollama não respondeu em {self.timeout} segundos.") from exc
        except (ValueError, TypeError) as exc:
            raise RuntimeError("Ollama retornou JSON inválido.") from exc
        answer = payload.get("response") if isinstance(payload, dict) else None
        if not isinstance(answer, str) or not answer.strip():
            raise RuntimeError("Ollama retornou uma resposta vazia ou inválida.")
        return answer.strip()
