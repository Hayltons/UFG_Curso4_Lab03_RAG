# Decisões técnicas do CAP02

Estas são escolhas iniciais para um MVP local e pedagógico. Versões de pacotes e comandos de instalação serão confirmados quando as dependências forem instaladas e exercitadas no CAP03. O CAP05 pode justificar ajustes de parâmetros; mudanças de tecnologia precisam de evidência.

| ID | Decisão | Motivo | Limite e verificação pendente |
| --- | --- | --- | --- |
| DT01 | Python 3.11 em `.venv`. | Ambiente já validado no CAP01; mantém execução isolada. | Fixar versões de dependências após instalação e testes no Windows. |
| DT02 | PyMuPDF para extrair texto por página. | API direta para abrir PDF e obter texto de cada página, sem framework RAG. | Ordem de leitura e páginas sem texto devem ser conferidas no PDF real; sem OCR. |
| DT03 | Sentence Transformers com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` como **candidato inicial** de embeddings. | Modelo multilíngue simples de usar, com vetores de 384 dimensões; adequado para começar a testar perguntas em português. | O modelo limita a entrada a 128 tokens. Medir truncamento na ingestão e avaliar recuperação no CAP05; sua adequação ao manual ainda não foi comprovada. |
| DT04 | `faiss-cpu` e `IndexFlatIP` em memória, com vetores de documento e pergunta normalizados. | Busca exata suficiente para um PDF; produto interno de vetores unitários corresponde à similaridade de cosseno. | Consome memória e reindexa ao reiniciar. Score não é probabilidade de resposta correta. |
| DT05 | Ollama local com `gemma3:4b` como LLM generativo baseline, configurável via ambiente. | Modelo já instalado e validado em português no notebook de referência. | O contexto de 4096 tokens e o uso de GPU foram observados naquele ambiente; verificar limites reais no CAP03. Reavaliar o LLM apenas se o CAP05 demonstrar limitação relevante de qualidade, desempenho ou contexto. |
| DT06 | Cliente Ollama HTTP pequeno, com biblioteca padrão de Python, inicialmente sem streaming. | Expõe chamada, timeout e erros sem dependência extra. | Tratar serviço/modelo indisponível e resposta inválida; não acoplar à GPU. |
| DT07 | Streamlit para interface mínima. | Permite perguntas e exibição de fontes com pouco código; o RAG permanece no serviço Python. | Avaliar cache de recursos apenas após observar recarregamento caro; recursos globais em cache exigem atenção ao uso concorrente. |
| DT08 | `python-dotenv` para configurações locais e `pytest` para testes. | Mantêm parâmetros fora do código e verificam contratos de componentes. | `.env` fica fora do Git; `.env.example` deve refletir opções reais ao final do CAP03. |
| DT09 | Sem LangChain e LlamaIndex na primeira versão. | Preserva a visibilidade de loader, chunker, embeddings, índice, retrieval, prompt e LLM para aprendizado. | Pequeno código de integração será escrito diretamente; evitar criar abstrações genéricas sem uso. |

## Parâmetros iniciais a validar

- `PDF_PATH`: `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`.
- `OLLAMA_MODEL`: `gemma3:4b`; modelo de embeddings configurado separadamente.
- `TOP_K=4`, `CHUNK_SIZE=350` caracteres e `CHUNK_OVERLAP=50` caracteres são pontos de partida, não resultados otimizados.
- Um limite de contexto configurável deverá reservar espaço para instruções, pergunta e resposta. Não usar integralmente a janela observada de 4096 tokens para trechos.
- Não fixar limiar de similaridade antes de avaliar perguntas dentro e fora do manual. Um corte arbitrário pode tanto descartar evidência útil quanto aceitar trecho irrelevante.

## Fontes técnicas consultadas

- [PyMuPDF: extração de texto](https://pymupdf.readthedocs.io/en/latest/recipes-text.html): extração por página e ressalvas sobre ordem de leitura.
- [Card do modelo multilíngue](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2): 50 idiomas, 384 dimensões e sequência máxima de 128 tokens.
- [FAISS: métricas e normalização](https://github.com/facebookresearch/faiss/wiki/MetricType-and-distances): produto interno em vetores normalizados para similaridade de cosseno.
- [PyPI: `faiss-cpu`](https://pypi.org/project/faiss-cpu/): há distribuição para CPython 3.11 no Windows x86-64; a instalação efetiva será testada no CAP03.
- [Ollama: API de geração](https://docs.ollama.com/api/generate): operação com modelo, prompt e opção `stream`.
- [Streamlit: cache de recursos](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource): compartilhamento de recursos e requisito de segurança em acesso concorrente.

O uso de um modelo multilíngue para perguntas em português é uma escolha inicial inferida do card do modelo, não uma validação de qualidade para este PDF. A avaliação do CAP05 decidirá se ele é suficiente.
