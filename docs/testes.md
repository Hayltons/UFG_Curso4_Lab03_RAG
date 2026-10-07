# Estratégia de testes e avaliação — CAP05

Os testes automatizados verificam contratos reproduzíveis sem chamar Ollama ou baixar o modelo de embeddings. Um modelo falso cobre a interface do `EmbeddingService`; FAISS e PyMuPDF reais exercitam os pontos em que a biblioteca importa. O conjunto manual em `tests/eval_cases.jsonl` usa o PDF real e o baseline `gemma3:4b` para avaliar qualidade de recuperação e resposta separadamente.

| Requisito | Verificação | Tipo | Prioridade |
| --- | --- | --- | --- |
| RF01–RF02 | `tests/test_ingestion.py`: PDF sintético válido, ausente, inválido e sem texto; origem e página. | Unidade/integração PyMuPDF | Alta |
| RF03 | `tests/test_ingestion.py`: limites, overlap, páginas e IDs. | Unidade | Alta |
| RF04 | `tests/test_retrieval.py`: quantidade, dimensão, finitude, entrada vazia e truncamento com modelo falso; smoke real no conjunto de avaliação. | Unidade + avaliação | Alta |
| RF05 | `tests/test_retrieval.py`: índice FAISS, normalização, vínculo vetor–chunk e rejeição de vetores inválidos. | Integração FAISS | Alta |
| RF06 | `tests/test_service.py` e `tests/test_frontend.py`: pergunta vazia não chega a embeddings/LLM. | Unidade/integração UI | Alta |
| RF07 | `tests/test_retrieval.py`: ordenação Top-K, score e metadados sem LLM; `tests/eval_cases.jsonl` verifica página esperada. | Unidade + avaliação | Alta |
| RF08 | `tests/test_service.py`: prompt e resposta do cliente falso; `tests/eval_cases.jsonl` avalia fundamentação real. | Unidade + avaliação | Alta |
| RF09 | `tests/test_service.py` e `tests/test_frontend.py`: fontes enviadas ao LLM e páginas na UI; avaliação confirma citações. | Integração + avaliação | Alta |
| RF10 | `tests/test_service.py`: sem contexto não chama LLM; casos fora do manual avaliam abstenção do modelo real. | Unidade + avaliação | Alta |
| RF11 | `tests/test_frontend.py`: formulário, resposta, fontes e erros com serviço falso. | Integração UI | Média |
| RNF01 | `pip check`, comando pytest e smoke test na `.venv`; reproduzibilidade completa revisada no CAP06. | Verificação de ambiente | Média |
| RNF02 | Testes isolados de loader, chunker, embeddings, store, prompt, cliente e serviço. | Revisão/automação | Média |
| RNF03 | `tests/test_config.py`: defaults, precedência de ambiente e rejeição de parâmetros inválidos. | Unidade | Alta |
| RNF04 | `tests/test_frontend.py`: serviço reaproveitado na sessão, PDF/LLM com erro exibido; `tests/test_service.py`: ingestão separada de consulta. | Integração | Alta |
| RNF05 | Suíte pytest, dataset auditável e relatório em `docs/avaliacao-rag.md`. | Automação + avaliação | Alta |

As perguntas de avaliação cobrem respostas explícitas, uma formulação ampla/ambígua e perguntas fora do conteúdo. Para cada caso, o [relatório RAG](avaliacao-rag.md) registra separadamente se a evidência correta entrou no Top-K, se os chunks enviados bastavam, se a resposta foi sustentada, se a citação correspondeu e se a recusa foi adequada. Não ajustar parâmetros ou trocar modelo automaticamente em resposta a falhas isoladas.

Na execução de fechamento do CAP05, `python -m pytest -q` aprovou **27 testes** e `python -m pip check` não encontrou dependências quebradas. Nenhum teste da suíte precisa de Ollama ou de download de modelo. A avaliação com o PDF real e `gemma3:4b` concluiu oito casos sem falha técnica, mas encontrou três respostas incompletas entre as cinco perguntas cobertas. Não há ferramenta de cobertura prevista no projeto; por isso, não se reporta percentual artificial. Os riscos residuais estão detalhados no relatório.
