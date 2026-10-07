# Lab03 — chatbot RAG sobre um manual PDF

Este projeto desenvolve um MVP educacional para consultar um único manual PDF em linguagem natural e receber respostas fundamentadas com indicação de fonte e página.

## Estado atual

CAP01 preparou o ambiente; CAP02 definiu escopo e arquitetura; CAP03 implementou o backend RAG em Python. A interface Streamlit pertence ao CAP04 e a suíte pytest/avaliação de qualidade ao CAP05. Consulte o [plano de implementação](plano-implementacao-lab03-atualizado.md) e o [roteiro de prompts](prompts-lab03-atualizado.md) para a sequência de capítulos.

O documento escolhido para o MVP é [`data/guia-pratico-engenharia-software-com-ia-generativa.pdf`](data/guia-pratico-engenharia-software-com-ia-generativa.pdf).

## Pré-requisitos e ambiente

- Python 3.11 e `pip`.
- Git.
- Ollama e o modelo `gemma3:4b` para a geração local.

No PowerShell, crie e ative o ambiente virtual caso ainda não exista:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip --version
```

Se a política do PowerShell impedir a ativação, execute diretamente `.\.venv\Scripts\python.exe`. Neste computador, a `.venv` foi verificada com Python 3.11.6; o `python` global aponta para Python 3.14.

Ollama 0.34.3 e `gemma3:4b` estão instalados. O plano registra uma validação prévia de geração em português e execução local em GPU. Esses dados são uma referência do notebook usado neste laboratório, não requisitos rígidos para outras máquinas.

Instale as dependências do backend, verifique o modelo Ollama e copie a configuração se quiser alterar os padrões:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama list
Copy-Item .env.example .env
```

O primeiro carregamento do modelo de embeddings baixa arquivos do Hugging Face; as execuções seguintes usam o cache local. `OLLAMA_MODEL` e `EMBEDDING_MODEL` são configurações distintas. O arquivo `.env` é opcional e ignorado pelo Git; veja [.env.example](.env.example) para os parâmetros disponíveis.

## Executar o backend

Com o serviço Ollama ativo, execute o smoke test reproduzível:

```powershell
.\.venv\Scripts\python.exe -m app.smoke_backend
```

Ele indexa o PDF, consulta uma pergunta coberta e outra fora do manual, e mostra trechos recuperados, scores, páginas, resposta e fontes consultadas. A API Python para outras perguntas é:

```python
from app.rag_service import create_service

service = create_service()
report = service.ingest()
result = service.ask("Como diagnosticar uma resposta incorreta em RAG?")
print(result.answer)
for source in result.sources:
    print(source.chunk.source, source.chunk.page, source.score)
```

`ingest()` deve ser chamado uma vez antes de `ask()`; o índice FAISS fica em memória e é reconstruído ao reiniciar. As fontes listam os trechos enviados ao LLM, não certificam por si só que cada trecho sustenta cada frase. O prompt pede recusa quando o contexto não contém a resposta; a qualidade será avaliada no CAP05.

## Estrutura do projeto

| Caminho | Finalidade |
| --- | --- |
| `app/` | Componentes e serviço do backend RAG; `smoke_backend.py` verifica o fluxo real. |
| `data/` | PDF do MVP e dados locais. |
| `tests/` | Testes automatizados planejados para o CAP05. |
| `docs/` | Escopo, requisitos, arquitetura, decisões, backlog e registro do backend. |
| `prompts/` | Template versionado da resposta RAG. |
| `.env.example` | Configuração opcional e valores padrão do backend. |
| `requirements.txt` | Dependências diretas do backend testadas com Python 3.11. |

As decisões do CAP02 estão em [escopo](docs/escopo.md), [requisitos](docs/requisitos.md), [arquitetura](docs/arquitetura.md), [decisões técnicas](docs/decisoes-tecnicas.md) e [backlog](docs/backlog.md). A verificação executada no CAP03 está em [docs/backend.md](docs/backend.md).
