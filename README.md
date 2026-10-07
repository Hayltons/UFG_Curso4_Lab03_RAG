# Lab03 — chatbot RAG sobre um manual PDF

Este projeto desenvolverá um MVP educacional para consultar um único manual PDF em linguagem natural e receber respostas fundamentadas com indicação de fonte e página.

## Estado atual

O CAP01 prepara o ambiente e a estrutura inicial. Ainda não há pipeline RAG, interface web nem suíte de testes. Consulte o [plano de implementação](plano-implementacao-lab03-atualizado.md) e o [roteiro de prompts](prompts-lab03-atualizado.md) para a sequência de capítulos.

O documento escolhido para o MVP é [`data/guia-pratico-engenharia-software-com-ia-generativa.pdf`](data/guia-pratico-engenharia-software-com-ia-generativa.pdf).

## Pré-requisitos e ambiente

- Python 3.11 e `pip`.
- Git.
- Ollama e o modelo `gemma3:4b` para a etapa de geração, quando o backend estiver implementado.

No PowerShell, crie e ative o ambiente virtual caso ainda não exista:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip --version
```

Se a política do PowerShell impedir a ativação, execute diretamente `.\.venv\Scripts\python.exe`. Neste computador, a `.venv` foi verificada com Python 3.11.6; o `python` global aponta para Python 3.14.

Ollama 0.34.3 e `gemma3:4b` estão instalados. O plano registra uma validação prévia de geração em português e execução local em GPU. Esses dados são uma referência do notebook usado neste laboratório, não requisitos rígidos para outras máquinas.

## Estrutura inicial

| Caminho | Finalidade |
| --- | --- |
| `app/` | Código da aplicação, definido a partir do CAP02. |
| `data/` | PDF do MVP e dados locais. |
| `tests/` | Testes automatizados futuros. |
| `docs/` | Escopo, arquitetura e decisões futuras. |
| `prompts/` | Prompts usados pelo produto, quando definidos. |
| `.env.example` | Exemplo inicial de configuração. |
| `requirements.txt` | Dependências a definir após as decisões técnicas. |

O CAP02 definirá escopo, requisitos, arquitetura, dependências e backlog. Instruções de execução do RAG e testes serão adicionadas quando essas funcionalidades existirem.
