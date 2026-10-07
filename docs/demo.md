# Demonstração do MVP RAG

Execute na raiz do repositório, com Python 3.11 na `.venv`. A instalação e as configurações estão no [README](../README.md). Use o PDF versionado, `gemma3:4b` e o baseline (`TOP_K=4`, chunks de 350 caracteres, overlap de 50, contexto de 2500 caracteres).

## Preparação

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip check
ollama list
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.address 127.0.0.1
```

Ollama deve estar ativo e listar `gemma3:4b`. Abra o endereço mostrado no terminal. Aguarde a preparação do manual; a primeira sessão carrega embeddings e constrói o índice. Nas consultas seguintes, o índice da sessão é reutilizado. Após a primeira consulta, `ollama ps` em outro terminal permite observar o modelo carregado.

## Perguntas e observação

Envie uma pergunta por vez. Compare resposta e referência com o PDF; a lista **Fontes consultadas** contém os trechos enviados ao modelo, inclusive quando houve recusa. Os resultados abaixo são expectativas e observações do CAP05, não respostas garantidas em cada execução.

| Ordem / caso | Pergunta | O que conferir |
| --- | --- | --- |
| 1 — C02 | Segundo o manual, como diagnosticar uma resposta incorreta em um sistema RAG? | p. 12: verificar primeiro se a evidência foi recuperada; depois distinguir ingestão/retrieval de prompt/geração. Caso positivo principal. |
| 2 — C04 | Qual é o efeito de chunks muito pequenos e muito grandes no RAG? | p. 12: perda de contexto versus mistura de assuntos/consumo de janela. |
| 3 — A01 | Que cuidados devo tomar ao usar IA no desenvolvimento? | Resposta limitada a cuidados do manual; páginas 2, 3 e 14 foram relevantes no baseline. |
| 4 — N01 | Qual é o preço atual do Bitcoin em reais? | Declarar que a informação não foi encontrada; não inventar preço. |
| 5 — N02 | Qual é o prazo legal brasileiro para auditoria de código gerado por IA? | Declarar insuficiência; p. 19 apresenta a pergunta como fora da base. |
| 6 — C01 | Quais são os seis elementos do CO-STAR? | p. 6 tem C/O/S/T/A/R. Limitação conhecida: o baseline respondeu só C/O/S e cortou a frase. |
| 7 — C03 | Qual fluxo de Git o guia recomenda antes e depois de uma mudança assistida por IA? | p. 11: `git status`, `git diff`, commit relacionado ao objetivo após testes/aprovação. Limitação conhecida: resposta terminou em “commit rel”. |
| 8 — C05 | Quais dimensões o guia recomenda avaliar em um sistema RAG? | p. 14: retrieval, suficiência, grounding, citação e abstenção. Limitação conhecida: p. 14 não foi recuperada e suficiência foi omitida. |

Teste também o envio em branco: a tela deve pedir uma pergunta sem chamar o modelo. Mostre os três casos incompletos como limitações aceitas para esta entrega, com correções posteriores no [README](../README.md#próximos-passos).

## Encerramento e alternativa sem interface

Encerre o Streamlit com `Ctrl+C`. Para uma demonstração rápida do pipeline no terminal:

```powershell
.\.venv\Scripts\python.exe -m app.smoke_backend
```

O comando usa C02 e N01 e mostra índice, chunks, scores, fontes e resposta. Para coletar novamente os oito casos, use `python -m tests.evaluate_rag` na `.venv`; ele substitui o arquivo de observações, que deve ser comparado com a versão anterior no Git. A [avaliação original](avaliacao-rag.md) permanece como referência do baseline.
