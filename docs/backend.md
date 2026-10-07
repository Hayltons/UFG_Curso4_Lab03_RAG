# Backend RAG — implementação e verificação do CAP03

O backend implementa dois fluxos separados. `RAGService.ingest()` extrai o PDF por página, divide o texto em trechos, mede truncamento no tokenizer, calcula embeddings e constrói o índice FAISS. `RAGService.ask()` codifica a pergunta, recupera até quatro trechos, monta o prompt versionado e chama o Ollama. A resposta inclui os trechos **consultados**, com score, arquivo e página.

As dependências diretas instaladas em Python 3.11.6 estão fixadas em `requirements.txt`: PyMuPDF 1.28.2, Sentence Transformers 6.1.0, FAISS CPU 1.15.1, NumPy 2.4.6 e python-dotenv 1.2.4. `pip check` terminou sem conflitos. O primeiro uso do modelo de embeddings fez download; o smoke test seguinte usou o cache local. O Ollama local tinha `gemma3:4b` instalado.

## Comportamento observado

Com `TOP_K=4`, `CHUNK_SIZE=350`, `CHUNK_OVERLAP=50` e `MAX_CONTEXT_CHARS=2500`, o comando `python -m app.smoke_backend` registrou 21 páginas com texto, 59 chunks, vetores de 384 dimensões e **zero chunks truncados** pelo limite de 128 tokens do modelo.

| Pergunta | Retrieval e contexto | Geração |
| --- | --- | --- |
| “Segundo o manual, como diagnosticar uma resposta incorreta em um sistema RAG?” | Primeiro resultado: p. 12, score 0,635; outros resultados: p. 12, 2 e 13. Quatro chunks foram enviados ao LLM; o primeiro contém a instrução de verificar se o trecho correto foi recuperado. | Respondeu para verificar primeiro a recuperação; se falhar, investigar ingestão/chunking/embedding/retrieval, e, se acertar, prompt/geração. Citou p. 12. |
| “Qual é o preço atual do Bitcoin em reais?” | Resultados de baixa similaridade nas p. 2, 9, 20 e 19 (scores de 0,113 a 0,077). Os quatro chunks foram enviados; nenhum traz cotação de Bitcoin. | Respondeu: “Não encontrei essa informação no manual consultado.” |

Não houve falha de retrieval, construção do contexto ou chamada ao Ollama nesses dois casos. A primeira consulta recuperou a evidência necessária; na segunda, a busca retornou vizinhos irrelevantes, como esperado para Top-K sem limiar, mas o prompt levou o modelo a declarar insuficiência. Scores medem proximidade vetorial, não probabilidade de correção. Um caso de recusa não garante recusa consistente; isso será avaliado no CAP05.

## Revisão do backend

- **Crítico:** nenhum defeito bloqueante observado no fluxo exercitado.
- **Importante:** `sources` representa trechos enviados ao LLM, inclusive em caso de recusa. A interface do CAP04 deve apresentá-los como “fontes consultadas” para evitar a impressão de que todos fundamentam a resposta.
- **Melhoria futura:** o chunker corta por caracteres e pode começar/terminar no meio de palavras. O caso coberto ainda recuperou a passagem correta; mudar a estratégia de chunking sem avaliação poderia alterar a recuperação. Comparar alternativas no CAP05 se os casos de avaliação mostrarem falha.
- **Risco de qualidade:** Top-K sempre pode devolver trechos irrelevantes e o LLM pode responder sem respaldo, apesar do prompt restritivo. O CAP05 deve medir recuperação, suficiência e recusa em mais perguntas antes de adotar limiar ou trocar modelos.

O índice fica em memória. Não há interface web, persistência vetorial ou suíte pytest nesta etapa; pertencem aos capítulos posteriores quando aplicável.
