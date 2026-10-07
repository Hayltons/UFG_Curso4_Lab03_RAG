# Lab03 — chatbot RAG sobre um manual PDF

Este projeto desenvolve um MVP educacional para consultar um único manual PDF em linguagem natural e receber respostas fundamentadas com indicação de fonte e página.

## Estado atual

O backend RAG em Python está implementado e validado com o PDF do MVP. A interface web e a avaliação sistemática ainda não foram implementadas.

O documento escolhido para o MVP é [`data/guia-pratico-engenharia-software-com-ia-generativa.pdf`](data/guia-pratico-engenharia-software-com-ia-generativa.pdf).

## Roadmap

| Capítulo | Entrega | Estado |
| --- | --- | --- |
| CAP01 — Fundamentos e ambiente | Preparar Python, Git, estrutura e PDF local. | Concluído |
| CAP02 — Escopo e arquitetura | Definir requisitos, componentes, decisões técnicas e backlog. | Concluído |
| CAP03 — Backend | Implementar ingestão, embeddings, FAISS, recuperação, Ollama e smoke test. | Concluído |
| CAP04 — Frontend | Criar interface Streamlit, integrá-la ao serviço RAG e cuidar da inicialização. | Próximo |
| CAP05 — Testes e qualidade | Criar testes pytest e avaliar recuperação, fundamentação, fontes e recusa. | Planejado |
| CAP06 — Entrega final | Consolidar README, demonstração, checklist e validação final. | Planejado |

Os critérios e dependências de cada tarefa estão no [backlog](docs/backlog.md). Consulte também o [plano de implementação](plano-implementacao-lab03-atualizado.md) e o [roteiro de prompts](prompts-lab03-atualizado.md). Cada capítulo termina com revisão, verificações, conventional commit e push antes de iniciar o seguinte.

## Stack

| Componente | Tecnologia | Papel no MVP |
| --- | --- | --- |
| Linguagem e ambiente | Python 3.11 em `.venv` | Execução local do backend. |
| Leitura do PDF | PyMuPDF | Extração de texto por página. |
| Embeddings | Sentence Transformers, modelo `paraphrase-multilingual-MiniLM-L12-v2` | Vetores dos trechos e das perguntas. |
| Busca vetorial | FAISS CPU (`IndexFlatIP`) | Índice em memória e recuperação Top-K por similaridade de cosseno. |
| Geração | Ollama com `gemma3:4b` | Resposta local a partir do contexto recuperado. |
| Configuração | `python-dotenv` e `.env` opcional | Parâmetros do PDF, modelos, chunking e consulta. |
| Interface e testes | Streamlit (CAP04) e pytest (CAP05) | Etapas planejadas; ainda não integram o MVP atual. |

As versões instaladas do backend estão em [requirements.txt](requirements.txt), e as justificativas das escolhas em [decisões técnicas](docs/decisoes-tecnicas.md). O cliente HTTP do Ollama usa a biblioteca padrão do Python; o projeto não usa LangChain nem LlamaIndex.

## Arquitetura

O backend separa ingestão e consulta. O `RAGService` coordena os componentes sem depender da futura interface Streamlit:

```text
Ingestão: PDF → PDF Loader → Chunker → Embedding Service → FAISS
Consulta: pergunta → Retriever (embedding + Top-K no FAISS) → Prompt Builder → Ollama → resposta + fontes consultadas
```

O PDF é indexado por `ingest()` antes das perguntas; `ask()` reutiliza o índice em memória. Cada trecho preserva arquivo e página, que acompanham os resultados da busca e a resposta. O prompt pede ao modelo que use somente o contexto recuperado e declare insuficiência quando ele não sustenta uma resposta. Veja o [diagrama e os contratos dos componentes](docs/arquitetura.md) para mais detalhes.

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
