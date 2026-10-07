# Requisitos e critérios de aceitação

Os requisitos descrevem o comportamento esperado do MVP. Testes automatizados verificam contratos determinísticos; os casos de qualidade de resposta serão avaliados separadamente no CAP05.

## Funcionais

| ID | Requisito | Critério de aceitação verificável |
| --- | --- | --- |
| RF01 | Carregar o PDF fixo do MVP. | A ingestão aceita `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`; arquivo ausente, inválido ou sem texto útil gera erro compreensível. |
| RF02 | Extrair texto e origem por página. | Cada página com texto produz conteúdo associado ao nome do arquivo e ao número de página iniciado em 1. |
| RF03 | Dividir texto em trechos. | Tamanho e sobreposição são configuráveis; nenhum trecho cruza páginas e cada um conserva origem, página e identificador. |
| RF04 | Gerar embeddings. | Há um vetor numérico finito por trecho não vazio; todos os vetores dos trechos e da pergunta têm a mesma dimensão. |
| RF05 | Indexar os trechos. | O índice FAISS recebe todos os vetores válidos e conserva o vínculo entre a posição no índice e o trecho com metadados. |
| RF06 | Receber pergunta em linguagem natural. | Pergunta não vazia segue para consulta; texto vazio ou só com espaços é rejeitado antes de chamar embeddings ou LLM. |
| RF07 | Recuperar os trechos Top-K. | Para uma pergunta válida, o Retriever devolve até `min(K, quantidade de trechos)` resultados ordenados por similaridade, com texto, score e metadados; não chama o LLM. |
| RF08 | Gerar resposta fundamentada. | O prompt inclui instrução de usar apenas o contexto recuperado, pergunta e referências; o serviço devolve o texto gerado pelo LLM. |
| RF09 | Exibir fontes. | A resposta do serviço inclui arquivo e página dos trechos entregues ao LLM; a interface mostra essas referências, sem atribuir páginas não recuperadas. |
| RF10 | Tratar contexto insuficiente. | Sem trechos utilizáveis, o serviço devolve uma declaração de falta de informação sem chamar o LLM; com trechos não pertinentes, o prompt pede recusa e o comportamento é verificado em caso de avaliação fora do manual. |
| RF11 | Disponibilizar interface web mínima. | Streamlit mostra nome do manual, aceita pergunta, exibe resposta/fontes e comunica erros; toda lógica RAG fica no serviço Python. |

## Não funcionais

| ID | Requisito | Critério de aceitação verificável |
| --- | --- | --- |
| RNF01 | Execução local reproduzível em Python 3.11. | README, `.env.example` e dependências correspondem aos comandos efetivamente testados no CAP06. |
| RNF02 | Componentes pequenos e testáveis. | Loader, Chunker, Embedding Service, Vector Store, Retriever, Prompt Builder e cliente Ollama podem ser testados isoladamente; ingestão e consulta funcionam sem Streamlit. |
| RNF03 | Configuração explícita. | Caminho do PDF, modelo de embeddings, parâmetros de chunking, Top-K, limite de contexto e modelo Ollama ficam centralizados; valores inválidos geram erro claro. |
| RNF04 | Recursos locais e erros previsíveis. | Perguntas não reindexam o PDF; falhas do PDF, embeddings e Ollama são comunicadas sem traceback cru na interface. |
| RNF05 | Qualidade auditável. | Suíte pytest cobre contratos críticos; dataset de avaliação registra perguntas, evidência esperada e páginas para analisar retrieval, fundamentação, fontes e recusa. |

RF10 representa uma meta de qualidade para perguntas fora do manual. A busca Top-K sempre pode devolver algum vizinho mesmo quando ele é irrelevante; por isso, a recusa não pode ser considerada garantida apenas por testes unitários ou por um score sem calibração.
