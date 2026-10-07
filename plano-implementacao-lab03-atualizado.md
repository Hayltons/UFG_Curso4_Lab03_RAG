# Plano de Implementação --- Lab03

## MVP Chatbot de Perguntas e Respostas com RAG

### Finalidade

Este documento funciona como **Plano de Implementação do MVP**: organiza
escopo, arquitetura, fases, entregáveis e critérios de conclusão do
Lab03. O roteiro operacional de prompts para o Codex está separado em
`prompts-lab03-atualizado.md`.

## 1. Visão do produto

Construir o MVP mais simples possível no qual o usuário possa fazer uma
pergunta ou solicitar orientação sobre um assunto contido em um manual
PDF, recebendo uma resposta gerada por LLM com base nos trechos
recuperados desse documento.

### Pergunta de sucesso do MVP

> O usuário consegue consultar um único PDF em linguagem natural e
> receber uma resposta fundamentada no conteúdo do documento?

## 2. Princípios de implementação

-   Priorizar aprendizado dos componentes internos de RAG.
-   Manter o escopo pequeno e verificável.
-   Separar ingestão/indexação de consulta.
-   Preservar metadados suficientes para indicar fontes.
-   Não introduzir frameworks RAG de alto nível na primeira versão.
-   Evitar abstrações prematuras.
-   Desenvolver incrementalmente, com revisão e commit ao final de cada
    capítulo.
-   Usar CO-STAR como metodologia de interação com o Codex.
-   Tratar testes de software e avaliação de qualidade do RAG como
    atividades distintas.

## 3. Escopo inicial

### Incluído

-   Um PDF local: `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`.
-   Extração de texto.
-   Chunking configurável.
-   Embeddings.
-   Índice vetorial.
-   Busca semântica Top-K.
-   Construção de contexto.
-   Prompt para resposta fundamentada.
-   LLM.
-   Interface web simples.
-   Indicação básica de fonte/página.
-   Testes automatizados dos componentes.
-   Pequeno conjunto de avaliação RAG.

### Fora do MVP

-   Autenticação e gestão de usuários.
-   Plataforma multiusuário.
-   Ingestão complexa de múltiplas fontes.
-   OCR.
-   Fine-tuning.
-   Agentes autônomos.
-   Memória conversacional longa.
-   Deploy de produção.
-   Observabilidade avançada.
-   Interface visual sofisticada.

## 4. Arquitetura conceitual

### Fluxo de ingestão

``` text
PDF
 ↓
PDF Loader
 ↓
Texto + metadados
 ↓
Chunker
 ↓
Chunks + metadados
 ↓
Embedding Model
 ↓
Vetores
 ↓
Vector Store
```

### Fluxo de consulta

``` text
Pergunta
 ↓
Embedding da pergunta
 ↓
Retriever / Vector Store
 ↓
Top-K chunks
 ↓
Prompt Builder
 ↓
LLM
 ↓
Resposta + fontes
 ↓
Interface Web
```

### Componentes propostos

-   **PDF Loader:** extrair texto e metadados por página.
-   **Chunker:** dividir o texto preservando origem.
-   **Embedding Service:** gerar vetores para chunks e perguntas.
-   **Vector Store:** indexar e consultar vetores.
-   **Retriever:** coordenar recuperação Top-K.
-   **Prompt Builder:** combinar instruções, contexto e pergunta.
-   **LLM Client:** comunicar-se com o modelo.
-   **RAG Service:** orquestrar ingestão e consulta.
-   **Streamlit UI:** receber pergunta e apresentar resposta/fontes.

## 5. Stack inicial sugerida

  Área                        Tecnologia
  --------------------------- -----------------------
  Linguagem                   Python 3.11
  Ambiente                    `.venv`
  PDF                         PyMuPDF
  Embeddings                  Sentence Transformers
  Vector Store                FAISS
  LLM                         Ollama
  Front-end                   Streamlit
  Configuração                python-dotenv
  Testes                      pytest
  Versionamento               Git
  Desenvolvimento assistido   Codex no VS Code

A escolha definitiva deve ser registrada no CAP02. LangChain/LlamaIndex
ficam fora da primeira versão para tornar visíveis as etapas do RAG.

### Validação prévia do LLM local

Antes do início efetivo da implementação, o notebook foi validado para
execução local do LLM via Ollama. O ambiente observado foi:

-   **CPU:** Intel Core i9-13900HX, 24 núcleos e 32 processadores
    lógicos.
-   **RAM:** 31,7 GB.
-   **GPU:** NVIDIA GeForce RTX 4070 Laptop com 8 GB de VRAM.
-   **Disco livre observado:** aproximadamente 447,3 GB.
-   **Ollama:** versão 0.34.3 instalada e operacional.
-   **Modelo escolhido:** `gemma3:4b`, já instalado localmente.
-   **Tamanho exibido por `ollama list`:** 3,3 GB.
-   **Execução observada em `ollama ps`:** `100% GPU`.
-   **Contexto observado:** 4096 tokens.
-   **Teste funcional:** geração de resposta curta em português do
    Brasil executada com sucesso e com atendimento à restrição de
    formato.

Também existe localmente `deepseek-r1:1.5b`, mas ele não será o modelo
principal do MVP. Não será instalado outro LLM nesta etapa.

**Decisão:** adotar Ollama + `gemma3:4b` como baseline do modelo
generativo do Lab03. A decisão só deverá ser reaberta se os testes do
CAP05 demonstrarem limitação relevante de qualidade, desempenho ou
contexto.

Essa decisão se refere ao **LLM generativo**. O modelo de embeddings é
um componente diferente do pipeline e continuará sendo
selecionado/configurado separadamente.

------------------------------------------------------------------------

# CAP01 --- FUNDAMENTOS, AMBIENTE E ESTRUTURA INICIAL

## Objetivo

Estabelecer uma base limpa, isolada, versionada e compreensível antes de
decidir ou implementar o pipeline.

## Atividades

1.  Validar Python 3.11 e `.venv`.
2.  Validar `pip`.
3.  Inicializar Git.
4.  Configurar `origin` para `https://github.com/Hayltons/UFG_Curso4_Lab03_RAG`.
5.  Criar `.gitignore`.
6.  Criar estrutura mínima do repositório e mover o PDF escolhido para `data/`.
7.  Criar `AGENTS.md`.
8.  Criar README inicial.
9.  Registrar a validação do runtime local Ollama e do `gemma3:4b`.
10. Revisar fundações.
11. Criar conventional commit e fazer push da milestone.

## Estrutura inicial esperada

``` text
06_Curso04_Lab03_RAG/
├── .venv/
├── app/
├── data/
│   └── guia-pratico-engenharia-software-com-ia-generativa.pdf
├── tests/
├── docs/
├── prompts/
├── .env.example
├── .gitignore
├── AGENTS.md
├── README.md
└── requirements.txt
```

## Entregáveis

-   Ambiente isolado.
-   Repositório Git.
-   Remoto `origin` configurado e milestone publicada no GitHub.
-   Estrutura inicial.
-   `.gitignore`.
-   `AGENTS.md`.
-   README inicial.
-   `requirements.txt` inicial.
-   Evidência de que Ollama + `gemma3:4b` estão aptos a servir como
    baseline local no hardware disponível.

## Critério de conclusão

O projeto está pronto para decisões de escopo/arquitetura, sem
funcionalidades RAG implementadas prematuramente.

------------------------------------------------------------------------

# CAP02 --- ESCOPO, ARQUITETURA E PLANEJAMENTO

## Objetivo

Definir o que será construído, como os componentes se relacionam e em
que ordem serão implementados.

## Atividades

1.  Formalizar objetivo e escopo.
2.  Registrar o que fica fora do MVP.
3.  Definir requisitos funcionais.
4.  Definir requisitos não funcionais.
5.  Criar critérios de aceitação.
6.  Desenhar arquitetura.
7.  Documentar fluxo de ingestão.
8.  Documentar fluxo de consulta.
9.  Registrar decisões tecnológicas, incluindo a decisão já validada de
    Ollama + `gemma3:4b` como LLM generativo baseline.
10. Criar backlog incremental.
11. Fazer revisão arquitetural.
12. Versionar milestone.

## Requisitos funcionais iniciais sugeridos

-   **RF01:** carregar um manual PDF definido para o MVP.
-   **RF02:** extrair texto e metadados úteis.
-   **RF03:** dividir conteúdo em chunks.
-   **RF04:** gerar embeddings dos chunks.
-   **RF05:** indexar embeddings.
-   **RF06:** receber pergunta em linguagem natural.
-   **RF07:** recuperar os chunks mais relevantes.
-   **RF08:** gerar resposta com base no contexto recuperado.
-   **RF09:** informar fonte/página quando disponível.
-   **RF10:** declarar ausência de informação quando o contexto não
    sustentar uma resposta.

## Entregáveis

-   `docs/escopo.md`.
-   `docs/requisitos.md`.
-   `docs/arquitetura.md`.
-   `docs/decisoes-tecnicas.md`.
-   `docs/backlog.md`.

## Critério de conclusão

É possível explicar o MVP, seus limites, requisitos, arquitetura e
sequência de implementação antes de escrever o núcleo do RAG.

------------------------------------------------------------------------

# CAP03 --- IMPLEMENTAÇÃO DO BACK-END

## Objetivo

Implementar e integrar o pipeline RAG de forma incremental e observável.

## Fases

### 3.1 Configuração

Centralizar caminhos, modelo de embeddings, Top-K, modelo LLM e
variáveis relevantes. Usar `gemma3:4b` como valor inicial do modelo
Ollama, preferencialmente configurável por variável de ambiente para
permitir experimentos futuros sem alterar código.

### 3.2 PDF Loader

``` text
PDF → texto + página/origem
```

Tratar arquivo inexistente, inválido e sem texto.

### 3.3 Chunking

``` text
texto → chunks
```

Parâmetros principais: - `chunk_size`; - `chunk_overlap`.

Preservar metadados.

### 3.4 Embeddings

``` text
chunk → embedding → vetor numérico
```

Validar quantidade e dimensionalidade.

### 3.5 Vector Store

``` text
chunks + vetores → FAISS
```

Manter vínculo entre índice e conteúdo/metadados.

### 3.6 Retriever

``` text
pergunta → embedding → similaridade → Top-K chunks
```

Retornar conteúdo, score e origem.

### 3.7 Prompt Builder

Estrutura básica:

``` text
Instruções
+
Contexto recuperado
+
Pergunta
→ prompt
```

O prompt deve instruir o modelo a não inventar respostas não sustentadas
pelo contexto.

### 3.8 LLM Client

Comunicação mínima com Ollama, incluindo erros de serviço/modelo
indisponível. O baseline é `gemma3:4b`, cuja execução local já foi
validada em `100% GPU`; o cliente não deve depender de detalhes
específicos da GPU nem acoplar o código a um único modelo.

### 3.9 RAG Service

Orquestração:

``` text
ask(question)
 ↓
retrieve
 ↓
build prompt
 ↓
LLM
 ↓
answer + sources
```

### 3.10 Smoke test

Executar pergunta com resposta presente e pergunta fora do conteúdo.
Confirmar também a comunicação real com Ollama + `gemma3:4b`; se houver
problema de execução, distinguir falha do runtime/LLM de falha de
retrieval.

## Entregáveis

-   Backend funcional.
-   Pipeline de ingestão.
-   Pipeline de consulta.
-   Tratamento básico de erros.
-   Resposta com fontes.
-   Revisão técnica do backend.

## Critério de conclusão

O RAG funciona sem depender da interface Streamlit e pode ser exercitado
diretamente por Python/teste manual.

------------------------------------------------------------------------

# CAP04 --- IMPLEMENTAÇÃO DO FRONT-END

## Objetivo

Disponibilizar uma interface web mínima para utilização do backend RAG.

## Interface proposta

``` text
┌──────────────────────────────────────┐
│             Chatbot RAG              │
│                                      │
│ Manual: [nome do manual]             │
│                                      │
│ Pergunte sobre o manual              │
│ [_________________________________]  │
│                                      │
│             [ Perguntar ]            │
│                                      │
│ Resposta                             │
│ ...                                  │
│                                      │
│ Fontes                               │
│ Página X                             │
└──────────────────────────────────────┘
```

## Atividades

1.  Criar aplicação Streamlit.
2.  Receber pergunta.
3.  Validar entrada.
4.  Chamar somente o RAG Service.
5.  Exibir resposta.
6.  Exibir fontes.
7.  Exibir erros compreensíveis.
8.  Avaliar cache/estado apenas para recursos caros.
9.  Revisar integração.
10. Versionar milestone.

## Regra arquitetural

O frontend não deve implementar retrieval, embeddings, prompt ou lógica
do LLM.

## Critério de conclusão

O usuário consegue executar o Streamlit, fazer uma pergunta e visualizar
resposta e fontes.

------------------------------------------------------------------------

# CAP05 --- TESTES E QUALIDADE

## Objetivo

Verificar tanto a correção do software quanto a qualidade mínima do
comportamento RAG.

## 5.1 Testes de software

### PDF Loader

-   arquivo válido;
-   arquivo inexistente;
-   texto extraído;
-   metadados preservados.

### Chunker

-   geração de chunks;
-   tamanho;
-   overlap;
-   metadados.

### Embeddings

-   número de embeddings;
-   dimensionalidade;
-   entradas inválidas.

### Vector Store / Retriever

-   indexação;
-   Top-K;
-   recuperação esperada;
-   metadados/score.

### Prompt Builder

-   contexto incluído;
-   pergunta incluída;
-   instrução de não inventar.

### RAG Service

-   pergunta válida;
-   pergunta vazia;
-   contexto disponível;
-   contexto insuficiente;
-   erro do LLM;
-   fontes retornadas.

## 5.2 Avaliação do RAG

Criar conjunto pequeno:

  Tipo                   Exemplo
  ---------------------- --------------------------------------
  Resposta explícita     informação claramente presente
  Resposta distribuída   informação em mais de um trecho
  Ambígua                pergunta com formulação menos direta
  Fora do manual         informação inexistente

Avaliar separadamente: 1. retrieval correto? 2. contexto suficiente? 3.
resposta fundamentada? 4. fonte coerente? 5. recusa adequada quando
necessário?

O `gemma3:4b` é o baseline da avaliação. Não trocar o LLM durante o
ajuste inicial do RAG, para evitar confundir efeitos de chunking,
embeddings, retrieval, prompt e geração. Comparações com outro modelo
ficam como experimento opcional somente depois de estabelecer uma
baseline estável.

## 5.3 Revisão de qualidade

-   DRY.
-   SRP.
-   legibilidade.
-   acoplamento.
-   tratamento de erros.
-   testabilidade.
-   dependências.
-   complexidade desnecessária.

## Entregáveis

-   Suíte pytest.
-   Dataset simples de avaliação.
-   Relatório de avaliação.
-   Revisão/refatoração aprovada.
-   Resultado de cobertura quando aplicável.

## Critério de conclusão

Testes críticos passam e limitações conhecidas do retrieval/geração
estão documentadas.

------------------------------------------------------------------------

# CAP06 --- ENTREGA FINAL

## Objetivo

Tornar o MVP reproduzível, demonstrável e tecnicamente revisado.

## Atividades

1.  Atualizar README final.
2.  Confirmar dependências.
3.  Confirmar `.env.example`.
4.  Documentar arquitetura final.
5.  Criar roteiro de demonstração.
6.  Criar checklist de release.
7.  Executar revisão técnica profunda.
8.  Corrigir apenas achados aprovados.
9.  Executar testes finais.
10. Executar smoke test.
11. Validar comandos do README.
12. Verificar Git.
13. Criar conventional commit final e fazer push para `origin`.

## README final

Deve conter: - objetivo; - escopo; - arquitetura; - stack; -
pré-requisitos; - instalação; - configuração; - Ollama/modelo; - PDF de
demonstração; - execução; - testes; - funcionamento do pipeline RAG; -
limitações; - troubleshooting; - evoluções futuras.

## Demonstração

Preparar 5--10 perguntas conhecidas, incluindo: - respostas fáceis; -
perguntas com diferentes formulações; - ao menos uma pergunta sem
resposta no manual.

## Release checklist

-   [ ] Python/ambiente reproduzível.
-   [ ] Dependências atualizadas.
-   [ ] `.env.example` atualizado.
-   [ ] PDF de demonstração disponível ou instrução para obtê-lo.
-   [ ] Pipeline de ingestão funcionando.
-   [ ] Retrieval funcionando.
-   [ ] Ollama disponível e `gemma3:4b` funcionando como LLM baseline.
-   [ ] Execução local do LLM validada ou procedimento de diagnóstico
    documentado.
-   [ ] Streamlit funcionando.
-   [ ] Fontes exibidas.
-   [ ] Pergunta sem evidência tratada.
-   [ ] Testes passando.
-   [ ] Avaliação executada.
-   [ ] README validado.
-   [ ] Arquitetura documentada.
-   [ ] Limitações documentadas.
-   [ ] Git limpo.

------------------------------------------------------------------------

# 6. Estratégia de evolução

A ordem dos capítulos é intencional:

``` text
CAP01 — preparar
   ↓
CAP02 — pensar e planejar
   ↓
CAP03 — construir o núcleo
   ↓
CAP04 — disponibilizar ao usuário
   ↓
CAP05 — verificar e avaliar
   ↓
CAP06 — consolidar e entregar
```

Cada capítulo deve terminar com revisão, correções aprovadas,
verificações/testes, conventional commit e push para `origin`.

# 7. CO-STAR no processo de desenvolvimento

CO-STAR orientará os prompts enviados ao Codex:

-   **C --- Context:** estado atual e restrições.
-   **O --- Objective:** tarefa específica.
-   **S --- Style:** modo de abordagem.
-   **T --- Tone:** tom desejado.
-   **A --- Audience:** destinatário do resultado.
-   **R --- Response:** formato da entrega.

CO-STAR é usado para orientar **o desenvolvimento com GenAI**. Ele não
substitui o Prompt Builder interno do chatbot RAG.

``` text
Desenvolvedor ──CO-STAR──► Codex ──► constrói/revisa o software

Usuário ──pergunta──► Retriever ──► contexto ──► Prompt Builder ──► LLM
```

# 8. Critério de sucesso final

O Lab03 estará concluído quando uma pessoa conseguir, seguindo o
README: 1. preparar o ambiente; 2. disponibilizar o PDF de demonstração;
3. iniciar os componentes necessários; 4. executar o Streamlit; 5. fazer
uma pergunta cuja resposta esteja no manual; 6. receber resposta
fundamentada com fonte; 7. fazer uma pergunta fora do conteúdo; 8.
receber tratamento adequado sem resposta inventada; 9. executar os
testes; 10. compreender as limitações e arquitetura do MVP.
