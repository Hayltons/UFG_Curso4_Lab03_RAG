# Escopo do MVP

## Objetivo

Permitir que uma pessoa faça perguntas em português sobre um único manual PDF local e receba uma resposta em português baseada nos trechos recuperados, com indicação de arquivo e página. O laboratório deve tornar visíveis as etapas de um pipeline RAG e permitir avaliar separadamente recuperação e geração.

## Dentro do escopo

- Manual fixo: `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`.
- Extração de texto por página, divisão em trechos com tamanho e sobreposição configuráveis e preservação da origem.
- Embeddings locais, índice vetorial FAISS em memória e recuperação semântica Top-K.
- Construção de contexto limitado, prompt de resposta fundamentada e geração por Ollama com `gemma3:4b` como baseline.
- Serviço Python com operações separadas de ingestão e consulta; interface Streamlit mínima para pergunta, resposta, fontes e erros.
- Testes de software e um conjunto pequeno de avaliação manual do RAG, inclusive perguntas fora do manual.

## Fora do escopo

OCR, múltiplos PDFs, upload pelo usuário, autenticação, multiusuário, histórico longo de conversa, agentes, fine-tuning, deploy de produção, persistência sofisticada do índice e interface elaborada.

## Premissas e restrições

- O PDF está no repositório e teve 21 páginas com texto extraído no CAP03, resultado confirmado no CAP06. Páginas vazias são ignoradas; documento inteiramente sem texto ou inválido gera diagnóstico claro. OCR permanece fora do MVP.
- O primeiro funcionamento é local. A instalação inicial das dependências e o primeiro download do modelo de embeddings podem exigir internet; as consultas usam componentes locais.
- Python 3.11, `.venv`, Ollama e `gemma3:4b` foram adotados no CAP01. O modelo de embeddings é independente do modelo generativo.
- A janela de contexto observada para o LLM foi de 4096 tokens no notebook de referência; o contexto enviado deve permanecer limitado e configurável. Esse valor observado não substitui a verificação do runtime no CAP03.
- A fonte exibida identifica trechos recuperados. Sua relevância foi examinada nos casos do [CAP05](avaliacao-rag.md); as limitações aceitas constam da [revisão final](revisao-final.md).

## Critérios de sucesso

1. Seguindo o README final, outra pessoa prepara o ambiente, inicia Ollama e abre a aplicação.
2. Uma pergunta coberta pelo manual produz resposta sustentada por trechos recuperados e exibe arquivo/página.
3. Uma pergunta sem evidência suficiente leva o assistente a declarar essa limitação, sem apresentar informação inventada como fato do manual.
4. É possível exercitar ingestão e consulta diretamente em Python, sem Streamlit, e verificar separadamente testes de software e avaliação de qualidade do RAG.

Os critérios 2 e 3 foram exercitados com casos conhecidos no CAP05 e repetidos no smoke do CAP06. Há três respostas incompletas na avaliação ampla, adiadas pelo responsável para após o MVP. Recuperação e recusa não são infalíveis; os limites da reprodução do ambiente estão no [checklist de entrega](release-checklist.md).
