# Decisões técnicas do CAP02

Estas são escolhas iniciais para um MVP local e pedagógico. As dependências diretas do backend e da interface foram instaladas e exercitadas nos CAP03 e CAP04; as versões usadas estão em `requirements.txt`. As pendências da tabela registram o estado da decisão original. A [avaliação CAP05](avaliacao-rag.md) e a [revisão CAP06](revisao-final.md) registram os resultados posteriores: o baseline foi mantido e as respostas incompletas ficaram para após a entrega, por decisão do responsável.

| ID | Decisão | Motivo | Limite e verificação pendente |
| --- | --- | --- | --- |
| DT01 | Python 3.11 em `.venv`. | Ambiente já validado no CAP01; mantém execução isolada. | Versões diretas fixadas no CAP03; dependências transitivas seguem o resolvedor do `pip`. |
| DT02 | PyMuPDF para extrair texto por página. | API direta para abrir PDF e obter texto de cada página, sem framework RAG. | Ordem de leitura e páginas sem texto devem ser conferidas no PDF real; sem OCR. |
| DT03 | Sentence Transformers com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` como **candidato inicial** de embeddings. | Modelo multilíngue simples de usar, com vetores de 384 dimensões; o smoke test recuperou a página esperada para uma pergunta em português. | O modelo limita a entrada a 128 tokens. Nenhum dos 59 trechos do PDF atual foi truncado com `CHUNK_SIZE=350`; qualidade ampla ainda depende do CAP05. |
| DT04 | `faiss-cpu` e `IndexFlatIP` em memória, com vetores de documento e pergunta normalizados. | Busca exata suficiente para um PDF; produto interno de vetores unitários corresponde à similaridade de cosseno. | Consome memória e reindexa ao reiniciar. Score não é probabilidade de resposta correta. |
| DT05 | Ollama local com `gemma3:4b` como LLM generativo baseline, configurável via ambiente. | Modelo já instalado e validado em português no notebook de referência. | O contexto de 4096 tokens e o uso de GPU foram observados naquele ambiente; verificar limites reais no CAP03. Reavaliar o LLM apenas se o CAP05 demonstrar limitação relevante de qualidade, desempenho ou contexto. |
| DT06 | Cliente Ollama HTTP pequeno, com biblioteca padrão de Python, inicialmente sem streaming. | Expõe chamada, timeout e erros sem dependência extra. | Tratar serviço/modelo indisponível e resposta inválida; não acoplar à GPU. |
| DT07 | Streamlit para interface mínima, com `st.session_state` por sessão. | Mantém o serviço e o índice entre reruns sem compartilhar um objeto mutável global entre usuários. | Cada sessão constrói seu próprio modelo/índice; a assinatura da configuração e do PDF provoca reconstrução quando mudam. |
| DT08 | `python-dotenv` para configurações locais e `pytest` para testes futuros. | Parâmetros ficam fora do código; o `.env` é relido para detectar mudanças na interface. | `.env` fica fora do Git; `.env.example` reflete as opções do backend. A suíte pytest pertence ao CAP05. |
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
- [PyPI: `faiss-cpu`](https://pypi.org/project/faiss-cpu/): distribuição para CPython 3.11 no Windows x86-64, instalada e exercitada no CAP03.
- [Ollama: API de geração](https://docs.ollama.com/api/generate): operação com modelo, prompt e opção `stream`.
- [Streamlit: cache de recursos](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource): compartilhamento de recursos e requisito de segurança em acesso concorrente.

O resultado positivo de uma pergunta no CAP03 não valida a qualidade para todo o PDF. O CAP05 registrou três respostas incompletas, mantidas como limitações aceitas para a entrega educacional no CAP06; o modelo e os parâmetros não foram otimizados para ocultar essas falhas.
