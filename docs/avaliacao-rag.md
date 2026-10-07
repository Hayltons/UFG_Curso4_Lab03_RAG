# Avaliação RAG — CAP05

Execução em 7 de outubro de 2026 com o PDF versionado do MVP, `gemma3:4b`, modelo de embeddings `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` e parâmetros padrão: `TOP_K=4`, `CHUNK_SIZE=350`, `CHUNK_OVERLAP=50`, `MAX_CONTEXT_CHARS=2500`. A ingestão produziu 21 páginas com texto, 59 chunks e vetores de 384 dimensões. Os oito casos terminaram sem falha técnica. As perguntas e critérios manuais estão em [`tests/eval_cases.jsonl`](../tests/eval_cases.jsonl); as observações brutas, com textos dos chunks, scores, respostas e fontes, em [`docs/avaliacao-rag-observacoes.jsonl`](avaliacao-rag-observacoes.jsonl).

O julgamento distingue presença da evidência **completa no Top-K**, suficiência dos chunks efetivamente enviados, resposta completa e apoiada nesses chunks, citação correta e abstenção. Encontrar a página esperada por si só não prova que o chunk contém toda a resposta. As fontes exibidas pela aplicação são os trechos consultados, não uma verificação automática de cada afirmação.

| Caso | Retrieval e contexto | Resposta, fonte e recusa | Julgamento |
| --- | --- | --- | --- |
| C01 — seis elementos CO-STAR | Parcial: p. 6 entrou no Top-K, mas `p6:c1` termina em “si” e a continuação com T/A/R não entrou; contexto insuficiente. | Responde só C/O/S, terminando em “si”; cita p. 6, que sustenta apenas a parte apresentada. | Incompleta; falha principal de recuperação do trecho completo. |
| C02 — diagnóstico de erro RAG | Correto: p. 12 aparece duas vezes e contém a sequência necessária; contexto suficiente. | Explica verificar retrieval antes de prompt/geração e cita p. 12. | Completa e fundamentada. |
| C03 — fluxo Git | Correto: `p11:c1` e `p11:c2` chegaram ao contexto; a segunda parte contém “commit relacionado ao objetivo”. | Responde `git status` e `git diff`, mas termina em “commit rel”; cita p. 11. | Incompleta apesar de contexto suficiente; falha na geração/uso do contexto. |
| C04 — tamanho de chunks | Correto: p. 12 contém os efeitos perguntados; contexto suficiente. | Explica perda de contexto e mistura de assuntos/janela; cita p. 12. | Completa e fundamentada para a pergunta. |
| C05 — dimensões de avaliação | Incorreto para a lista completa: p. 14 não entrou; p. 21 traz uma lista parcial, sem “suficiência do contexto”; contexto insuficiente. | Lista retrieval, grounding, fontes e abstenção; omite suficiência; citação p. 21 sustenta apenas essa lista parcial. | Incompleta; falha principal de retrieval. |
| A01 — cuidados ao usar IA | Páginas 2, 3 e 14 trazem cuidados relevantes; a pergunta ampla não tem lista única exaustiva. | Resposta limitada à responsabilidade humana, validação e qualidade/segurança, com citações coerentes. | Adequada para uma pergunta ambígua. |
| N01 — preço atual do Bitcoin | Nenhum chunk fornece a cotação; contexto insuficiente. | Declara que não encontrou a informação, sem número ou fonte inventada. | Abstenção adequada. |
| N02 — prazo legal de auditoria | p. 19 classifica explicitamente a pergunta como fora da base; não há prazo no contexto. | Declara que não encontrou a informação e cita p. 19. | Abstenção adequada. |

Entre as cinco perguntas com resposta explícita, 3/5 tiveram evidência completa no contexto (C02–C04), mas só 2/5 receberam resposta completa e fundamentada (C02 e C04). A pergunta ampla recebeu resposta limitada aos trechos, e as duas perguntas fora do manual tiveram abstenção adequada (2/2). Esses números descrevem apenas este pequeno conjunto manual e uma execução do LLM; não são taxa geral de acerto. Nenhuma resposta observada inventou uma fonte, mas C01, C03 e C05 ficaram incompletas.

O conjunto foi conferido contra o PDF. Em A01, a lista inicial de páginas esperadas era estreita demais; após inspeção manual, foram incluídas as páginas 2, 3 e 14, que também contêm cuidados pertinentes. A pergunta, saída e parâmetros da execução não mudaram. Não houve ajuste de `TOP_K`, chunking, prompt ou troca de modelo após observar as falhas.

## Hipóteses e revisão conservadora

O corte por janela de caracteres atravessa palavras e listas. Em C01, o chunk seguinte ficou fora do Top-K; em C03, os dois chunks chegaram, mas separados por trechos menos relevantes, e a geração repetiu apenas o fragmento inicial. Em C05, a busca semântica trouxe a lista mais curta da p. 21, deixando fora a lista completa da p. 14. Repetições diagnósticas diretas do mesmo prompt no Ollama terminaram normalmente (`done_reason=stop`) e reproduziram as respostas parciais de C01/C03; o limite de saída da API não explica esses dois casos. Isso não prova uma causa única para a escolha do modelo.

O código mantém responsabilidades separadas entre loader, chunker, embeddings, store, retriever, composição do prompt, cliente Ollama, serviço e interface. Não apareceu duplicação ou acoplamento que justifique uma refatoração estrutural neste capítulo. Propostas para avaliação posterior, **não implementadas**:

| Proposta | Benefício esperado | Risco e arquivos afetados |
| --- | --- | --- |
| Comparar chunking em limites de frase/parágrafo ou expansão de chunks vizinhos nos casos C01/C05. | Evitar evidência partida e ampliar recall da lista correta. | Mais contexto, custo e possíveis trechos irrelevantes; `app/chunker.py`, `app/retriever.py`, `app/rag_service.py` e testes. |
| Ordenar/agrupar trechos adjacentes da mesma página antes de montar o prompt, preservando rastreabilidade. | Reduzir a quebra de continuidade observada em C03. | Alterar a prioridade por score e estourar o orçamento de contexto; `app/prompt_builder.py` e testes. |
| Registrar metadados de parada da geração no coletor de avaliação. | Distinguir respostas interrompidas por limite das terminadas pelo modelo. | Mudança no contrato do cliente se feita na aplicação; `tests/evaluate_rag.py` ou `app/ollama_client.py` e testes. |

Para reproduzir na raiz do projeto, com Ollama ativo e `gemma3:4b` disponível:

```powershell
.\.venv\Scripts\python.exe -m tests.evaluate_rag
```

O comando reindexa o PDF e substitui o arquivo de observações. O modelo generativo pode variar entre execuções; reavaliar as linhas antes de reutilizar os julgamentos deste relatório.
