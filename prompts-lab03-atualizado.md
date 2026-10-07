# Lab03 --- Roteiro de Execução com Prompts CO-STAR para Codex

## Projeto

**MVP Chatbot de Perguntas e Respostas com RAG sobre um manual em PDF**

## Objetivo deste roteiro

Conduzir a implementação incremental do Lab03 no Codex/VS Code, usando a
metodologia CO-STAR e preservando o caráter educacional do projeto. O
MVP deve permanecer simples, legível e verificável.

## Premissas do projeto

-   Python 3.11.
-   Ambiente virtual local `.venv`.
-   Um único PDF local no MVP: `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`.
-   Interface web simples com Streamlit.
-   Extração de PDF com PyMuPDF.
-   Embeddings com Sentence Transformers.
-   Vector Store com FAISS.
-   LLM local via Ollama, com `gemma3:4b` como modelo generativo
    baseline.
-   Hardware já validado: Intel Core i9-13900HX, 31,7 GB RAM e NVIDIA
    GeForce RTX 4070 Laptop com 8 GB de VRAM.
-   Ollama 0.34.3 já validado; `gemma3:4b` executou em `100% GPU`,
    contexto 4096, e respondeu corretamente em português do Brasil.
-   `deepseek-r1:1.5b` também está instalado, mas não é o modelo
    principal.
-   Não instalar ou trocar o LLM sem evidência de necessidade; reavaliar
    a escolha somente se os testes de qualidade indicarem limitação.
-   O LLM generativo e o modelo de embeddings são componentes distintos.
-   Testes com pytest.
-   Sem LangChain ou LlamaIndex na primeira versão.
-   Separar claramente ingestão/indexação, recuperação e geração.
-   O assistente deve responder com base no contexto recuperado e
    informar quando a resposta não estiver no manual.
-   Mudanças devem ser pequenas, testáveis e revisadas antes de avançar.
-   Usar `https://github.com/Hayltons/UFG_Curso4_Lab03_RAG` como remoto `origin`.
-   Fechar cada capítulo com um conventional commit e push para o remoto.

------------------------------------------------------------------------

# CAP01 --- FUNDAMENTOS, AMBIENTE E ESTRUTURA INICIAL

## Prompt 01 --- Inspecionar o ambiente e o diretório

**C --- Contexto:** Estamos iniciando o Lab03, um MVP educacional de
chatbot RAG sobre um único manual em PDF. O projeto está em um diretório
novo, com `.venv` criado em Python 3.11. O notebook já foi validado para
LLM local: Intel Core i9-13900HX, 31,7 GB RAM, RTX 4070 Laptop 8 GB
VRAM, Ollama 0.34.3 e `gemma3:4b` executando em `100% GPU` com contexto
4096.

**O --- Objetivo:** Inspecione o diretório atual e o ambiente Python.
Não altere arquivos ainda. Identifique versão do Python, ambiente
virtual, Git, arquivos existentes e possíveis riscos de configuração.

**S --- Estilo:** Análise técnica curta, verificável e conservadora. Não
proponha arquitetura complexa.

**T --- Tom:** Técnico, didático e objetivo.

**A --- Audiência:** Desenvolvedor estudando Engenharia de Software com
GenAI e RAG.

**R --- Resposta:** Entregue: (1) estado atual; (2) problemas
encontrados; (3) comandos de verificação executados; (4) próximos passos
recomendados. Não implemente nada sem necessidade.

------------------------------------------------------------------------

## Prompt 02 --- Inicializar Git e criar `.gitignore`

**C:** O diretório foi validado e será usado exclusivamente para o
Lab03. O `.venv` não deve ser versionado.

**O:** Inicialize o repositório Git, se necessário, configure `origin`
para `https://github.com/Hayltons/UFG_Curso4_Lab03_RAG` e crie um
`.gitignore` adequado a Python, VS Code, pytest, variáveis de ambiente,
caches e artefatos locais do RAG. Não ignore arquivos de código,
documentação, testes ou o PDF do MVP. Confira o estado e a branch do
remoto antes do primeiro push.

**S:** Configuração mínima e explícita.

**T:** Técnico e direto.

**A:** Desenvolvedor Python em ambiente Windows/VS Code.

**R:** Faça as alterações e mostre um resumo do `.gitignore`,
justificando grupos relevantes. Ao final, execute `git status`.

------------------------------------------------------------------------

## Prompt 03 --- Criar a estrutura inicial

**C:** O projeto é um MVP educacional. A arquitetura detalhada será
definida no CAP02; portanto, agora precisamos apenas de uma estrutura
inicial sem antecipar abstrações.

**O:** Crie somente a estrutura mínima: `app/`, `data/`, `tests/`,
`docs/`, `prompts/`, além de `README.md`, `AGENTS.md`, `.env.example` e
`requirements.txt`. Mova o arquivo
`guia-pratico-engenharia-software-com-ia-generativa.pdf` para `data/`
e atualize suas referências. Adicione `__init__.py` apenas onde
necessário.

**S:** Estrutura enxuta. Evite criar módulos de domínio antes da
definição arquitetural.

**T:** Técnico e disciplinado.

**A:** Desenvolvedor que deseja acompanhar cada decisão do MVP.

**R:** Crie a estrutura, apresente a árvore resultante e explique em uma
frase a finalidade de cada diretório/arquivo.

------------------------------------------------------------------------

## Prompt 04 --- Criar `AGENTS.md`

**C:** O Codex será usado iterativamente durante todo o Lab03.
Precisamos de regras persistentes para impedir crescimento desnecessário
do escopo.

**O:** Crie `AGENTS.md` com orientações específicas do projeto: Python
3.11; simplicidade; alterações pequenas; não adicionar dependências sem
justificativa; separar ingestão, retrieval e geração; executar testes;
não introduzir LangChain/LlamaIndex nesta versão; não alterar escopo sem
aprovação; preservar legibilidade e documentação.

**S:** Regras operacionais claras e concisas.

**T:** Normativo, mas didático.

**A:** Codex e futuros colaboradores do projeto.

**R:** Grave o arquivo e apresente os princípios mais importantes em
checklist.

------------------------------------------------------------------------

## Prompt 05 --- Criar README inicial

**C:** Ainda não definimos toda a arquitetura. O README desta etapa deve
registrar apenas informações já decididas.

**O:** Crie um README inicial contendo objetivo do Lab03,
pré-requisitos, criação/ativação do `.venv`, Python 3.11, estrutura
inicial, caminho do PDF em `data/` e estado atual. Registre também como premissa já validada o uso
local de Ollama + `gemma3:4b`, sem transformar o README em relatório de
benchmark. Marque arquitetura, execução do RAG e testes detalhados como
seções a completar.

**S:** Documentação técnica enxuta e reproduzível.

**T:** Claro e profissional.

**A:** Aluno/desenvolvedor que retomará o projeto posteriormente.

**R:** Atualize `README.md` sem inventar funcionalidades ainda
inexistentes.

------------------------------------------------------------------------

### Evidência prévia a preservar no CAP01

A validação de hardware/runtime já foi executada antes do início do
Codex e não precisa ser repetida sem motivo. Evidências disponíveis para
documentação:

-   `ollama --version` → 0.34.3;
-   `ollama list` → `gemma3:4b` (3,3 GB) e `deepseek-r1:1.5b` (1,1 GB);
-   `ollama run gemma3:4b` → resposta em português do Brasil
    bem-sucedida;
-   `ollama ps` → `gemma3:4b`, `100% GPU`, contexto 4096;
-   hardware → i9-13900HX, 31,7 GB RAM, RTX 4070 Laptop 8 GB VRAM.

Esses dados são baseline de ambiente, não requisito rígido para futuras
máquinas que venham a executar o repositório.

------------------------------------------------------------------------

## Prompt 06 --- Revisão do CAP01

**C:** O CAP01 deve conter apenas fundações de ambiente e estrutura.

**O:** Revise o estado atual sem adicionar funcionalidades. Verifique
ambiente, Git, `.gitignore`, estrutura, `AGENTS.md`, README e sinais de
complexidade prematura.

**S:** Code review orientado a riscos.

**T:** Crítico e construtivo.

**A:** Desenvolvedor preparando o projeto para arquitetura e
implementação.

**R:** Checklist classificado em `Crítico`, `Importante` e
`Melhoria futura`. Para cada achado, indique arquivo e ação recomendada.
Não faça alterações.

------------------------------------------------------------------------

## Prompt 07 --- Consolidar e versionar CAP01

**C:** A revisão do CAP01 foi analisada e os ajustes aprovados devem
estar concluídos.

**O:** Execute verificações finais, mostre `git diff`/`git status`
resumidos, crie um conventional commit para o CAP01 e faça push para
`origin` na branch verificada. A autorização para esse push já foi dada
na conversa do projeto.

**S:** Procedimento de encerramento de etapa.

**T:** Objetivo.

**A:** Desenvolvedor usando Git como trilha de evolução do laboratório.

**R:** Informe os arquivos versionados, o hash do commit, a branch e o
resultado do push. Mensagem sugerida: `chore: preparar estrutura inicial do Lab03`.

------------------------------------------------------------------------

# CAP02 --- ESCOPO, ARQUITETURA E PLANEJAMENTO

## Prompt 08 --- Definir escopo do MVP

**C:** O objetivo é aprender RAG e Engenharia de Software, não construir
uma plataforma completa.

**O:** Proponha e documente o escopo do MVP: um PDF local, perguntas em
linguagem natural, ingestão, chunking, embeddings, FAISS, recuperação
Top-K, LLM, resposta fundamentada, fonte simples e Streamlit. Explicite
também o que ficará fora do MVP.

**S:** Product/engineering scope conciso, evitando scope creep.

**T:** Analítico.

**A:** Desenvolvedor e revisor técnico.

**R:** Crie `docs/escopo.md` com objetivo, dentro do escopo, fora do
escopo, premissas, restrições e critérios de sucesso.

------------------------------------------------------------------------

## Prompt 09 --- Definir requisitos

**C:** O escopo do MVP está aprovado.

**O:** Derive requisitos funcionais e não funcionais mínimos. Numere-os
(`RF01...`, `RNF01...`). Inclua ingestão do PDF, chunking, embeddings,
armazenamento vetorial, consulta, recuperação, geração, tratamento de
pergunta sem resposta e exibição de fonte.

**S:** Especificação simples, testável e rastreável.

**T:** Formal o suficiente para orientar testes, sem burocracia
excessiva.

**A:** Desenvolvedor e testador do MVP.

**R:** Crie `docs/requisitos.md`, incluindo critérios de aceitação
verificáveis para cada requisito relevante.

------------------------------------------------------------------------

## Prompt 10 --- Propor arquitetura

**C:** Escopo e requisitos estão definidos. Queremos enxergar
explicitamente cada etapa do RAG.

**O:** Proponha uma arquitetura mínima separando: PDF Loader, Chunker,
Embedding Service, Vector Store, Retriever, Prompt Builder, LLM Client e
RAG Service. Evite camadas que não agreguem valor ao MVP.

**S:** Arquitetura modular, simples e pedagógica.

**T:** Técnico e justificativo.

**A:** Desenvolvedor estudando os componentes internos de RAG.

**R:** Crie `docs/arquitetura.md` com responsabilidades, fluxo de
ingestão, fluxo de consulta, dependências entre componentes e um
diagrama Mermaid.

------------------------------------------------------------------------

## Prompt 11 --- Registrar decisões tecnológicas

**C:** A stack candidata é Python 3.11, PyMuPDF, Sentence Transformers,
FAISS, Ollama, Streamlit, python-dotenv e pytest. A parte generativa já
possui evidência local: Intel Core i9-13900HX, 31,7 GB RAM, RTX 4070
Laptop 8 GB, Ollama 0.34.3 e `gemma3:4b` executando em `100% GPU`,
contexto 4096, com resposta em português validada. `deepseek-r1:1.5b`
também está instalado, mas não foi escolhido como baseline.

**O:** Avalie essa stack para o escopo definido. Registre vantagens,
limitações e justificativas. Formalize Ollama + `gemma3:4b` como decisão
inicial do LLM generativo, distinguindo-o do modelo de embeddings. Não
substitua tecnologias nem proponha outro LLM sem demonstrar necessidade.
Registre como condição de reavaliação evidência obtida no CAP05 de
limitação relevante de qualidade, desempenho ou contexto.

**S:** Registro de decisão arquitetural enxuto.

**T:** Técnico e comparativo.

**A:** Desenvolvedor que precisa compreender por que cada tecnologia foi
escolhida.

**R:** Crie `docs/decisoes-tecnicas.md`. Destaque que frameworks RAG de
alto nível ficam fora da primeira versão para preservar transparência
didática.

------------------------------------------------------------------------

## Prompt 12 --- Planejar backlog incremental

**C:** Arquitetura e decisões foram definidas.

**O:** Transforme o trabalho dos CAP03--CAP06 em backlog incremental,
com tarefas pequenas, dependências e critérios de pronto. Priorize
primeiro uma vertical mínima funcional e depois qualidade.

**S:** Planejamento de engenharia pragmático.

**T:** Objetivo.

**A:** Desenvolvedor executando o laboratório sozinho com apoio do
Codex.

**R:** Crie `docs/backlog.md` com IDs, descrição, dependências, critério
de pronto e capítulo associado.

------------------------------------------------------------------------

## Prompt 13 --- Revisão arquitetural do CAP02

**C:** Temos escopo, requisitos, arquitetura, decisões e backlog.

**O:** Faça uma revisão crítica procurando: complexidade prematura,
requisitos não cobertos, acoplamento excessivo, abstrações
desnecessárias, decisões sem justificativa e riscos para testes.

**S:** Architecture review sem implementação.

**T:** Crítico e construtivo.

**A:** Desenvolvedor antes de iniciar o código do RAG.

**R:** Relatório em checklist com severidade e recomendação. Não altere
arquivos.

------------------------------------------------------------------------

## Prompt 14 --- Consolidar e versionar CAP02

**C:** Os ajustes aprovados da revisão foram aplicados.

**O:** Verifique consistência entre escopo, requisitos, arquitetura e
backlog. Mostre `git status`, crie um conventional commit e faça push
para `origin` na branch do projeto.

**S:** Fechamento de milestone.

**T:** Conciso.

**A:** Desenvolvedor.

**R:** Informe hash e resultado do push. Mensagem sugerida:
`docs: definir escopo e arquitetura do MVP`.

------------------------------------------------------------------------

# CAP03 --- IMPLEMENTAÇÃO DO BACK-END

## Prompt 15 --- Implementar configuração

**C:** A arquitetura foi aprovada. Precisamos iniciar o backend pelas
configurações, sem implementar RAG completo de uma vez.

**O:** Implemente configuração mínima para caminhos, modelo de
embeddings, Top-K, modelo Ollama e parâmetros essenciais, usando
variáveis de ambiente quando apropriado. Configure `gemma3:4b` como
baseline/default do LLM sem hard-code espalhado pelo projeto. Atualize
`.env.example`. Não confunda a configuração do LLM com a do modelo de
embeddings.

**S:** Código Python simples, tipado quando útil, sem framework de
configuração pesado.

**T:** Técnico.

**A:** Desenvolvedor Python.

**R:** Implemente, mostre arquivos alterados e inclua validações para
configurações obrigatórias.

------------------------------------------------------------------------

## Prompt 16 --- Implementar PDF Loader

**C:** O MVP usa `data/guia-pratico-engenharia-software-com-ia-generativa.pdf`.

**O:** Implemente um componente que valide o arquivo, extraia texto por
página com PyMuPDF e preserve metadados mínimos de origem/página para
futura citação.

**S:** Função/classe pequena e testável.

**T:** Técnico e didático.

**A:** Desenvolvedor aprendendo ingestão de documentos.

**R:** Implemente somente o loader. Inclua tratamento de arquivo
inexistente, PDF inválido e documento sem texto. Não implemente chunking
ainda.

------------------------------------------------------------------------

## Prompt 17 --- Implementar Chunker

**C:** O loader produz texto com referência de página.

**O:** Implemente chunking simples e transparente, com `chunk_size` e
`chunk_overlap` configuráveis. Preserve metadados de origem/página.

**S:** Algoritmo compreensível, evitando abstrações externas
desnecessárias.

**T:** Técnico.

**A:** Desenvolvedor estudando impacto de chunking em RAG.

**R:** Implemente e demonstre com uma pequena entrada de exemplo quantos
chunks são gerados e quais metadados são preservados.

------------------------------------------------------------------------

## Prompt 18 --- Implementar Embedding Service

**C:** Temos chunks textuais e precisamos convertê-los em vetores.

**O:** Implemente o serviço de embeddings com Sentence Transformers.
Centralize o nome do modelo na configuração e permita gerar embeddings
para documentos e pergunta.

**S:** Interface pequena e explícita.

**T:** Técnico.

**A:** Desenvolvedor estudando embeddings.

**R:** Implemente e inclua verificações simples de dimensão, quantidade
de vetores e erros de entrada.

------------------------------------------------------------------------

## Prompt 19 --- Implementar Vector Store FAISS

**C:** Os chunks possuem embeddings.

**O:** Implemente armazenamento/indexação com FAISS, mantendo mapeamento
entre vetor e chunk/metadados. Permita construir o índice e consultar
Top-K.

**S:** Implementação mínima, sem camada de persistência sofisticada.

**T:** Técnico.

**A:** Desenvolvedor estudando busca vetorial.

**R:** Implemente e demonstre uma consulta simples. Explique brevemente
qual métrica de similaridade está sendo usada e como isso afeta o
resultado.

------------------------------------------------------------------------

## Prompt 20 --- Implementar Retriever

**C:** O Vector Store consegue retornar vizinhos próximos.

**O:** Implemente o Retriever responsável por receber uma pergunta,
gerar seu embedding, consultar Top-K e devolver chunks relevantes com
score e metadados.

**S:** Separação clara de responsabilidade.

**T:** Técnico.

**A:** Desenvolvedor estudando retrieval.

**R:** Implemente sem chamar LLM. Mostre um exemplo de resultado de
retrieval.

------------------------------------------------------------------------

## Prompt 21 --- Implementar Prompt Builder

**C:** O Retriever fornece os trechos relevantes.

**O:** Implemente um Prompt Builder que instrua o LLM a responder
somente com base no contexto recuperado, declarar quando não houver
informação suficiente e evitar inventar dados. Inclua pergunta, contexto
e referências.

**S:** Prompt legível, versionável e simples.

**T:** Claro e restritivo.

**A:** LLM que responderá sobre o manual.

**R:** Implemente o prompt em local fácil de revisar e mostre um exemplo
renderizado com dados fictícios.

------------------------------------------------------------------------

## Prompt 22 --- Implementar cliente Ollama

**C:** O modelo local será acessado pelo Ollama. O nome do modelo deve
vir da configuração. O baseline já validado é `gemma3:4b`, executando
localmente em `100% GPU` no notebook; portanto, não é necessário
instalar outro modelo nem implementar lógica específica de GPU.

**O:** Implemente um cliente mínimo para enviar o prompt ao Ollama,
tratar indisponibilidade do serviço/modelo e devolver texto da resposta.
Use `gemma3:4b` via configuração e mantenha o wrapper agnóstico o
bastante para permitir uma troca futura de modelo por configuração, se o
CAP05 justificar.

**S:** Wrapper fino; não esconda comportamento relevante.

**T:** Técnico.

**A:** Desenvolvedor local.

**R:** Implemente e inclua uma verificação clara de erro quando o Ollama
ou o modelo não estiver disponível.

------------------------------------------------------------------------

## Prompt 23 --- Implementar RAG Service

**C:** Loader, chunker, embeddings, store, retriever, prompt e LLM estão
disponíveis.

**O:** Crie o serviço de orquestração do RAG separando
ingestão/indexação de consulta. A consulta deve retornar resposta e
fontes/chunks utilizados.

**S:** Orquestração simples; componentes permanecem testáveis
isoladamente.

**T:** Técnico.

**A:** Backend do MVP.

**R:** Implemente uma API Python simples, por exemplo `ask(question)`,
sem criar frontend ainda.

------------------------------------------------------------------------

## Prompt 24 --- Smoke test do backend

**C:** O pipeline backend está integrado.

**O:** Execute um teste manual ponta a ponta com
`data/guia-pratico-engenharia-software-com-ia-generativa.pdf`:
indexe, faça uma pergunta cuja resposta exista e outra cuja resposta não
exista. Use Ollama + `gemma3:4b` como baseline e diferencie
explicitamente falhas de retrieval, construção de contexto e geração.

**S:** Verificação funcional, não refatoração.

**T:** Investigativo.

**A:** Desenvolvedor antes de integrar frontend.

**R:** Mostre pergunta, chunks recuperados, fonte, resposta e eventuais
erros. Não masque falhas.

------------------------------------------------------------------------

## Prompt 25 --- Revisão do backend

**C:** O backend RAG está funcional.

**O:** Revise responsabilidades, acoplamento, tratamento de erros,
dependências, configuração, legibilidade e risco de hallucination.
Verifique se o código continua compatível com o escopo.

**S:** Code review sem mudanças automáticas.

**T:** Crítico e construtivo.

**A:** Desenvolvedor.

**R:** Achados por severidade, com arquivo/trecho e correção proposta.

------------------------------------------------------------------------

## Prompt 26 --- Consolidar e versionar CAP03

**C:** Correções aprovadas foram aplicadas.

**O:** Execute verificações do backend, crie um conventional commit e
faça push para `origin`.

**S:** Fechamento de etapa.

**T:** Objetivo.

**A:** Desenvolvedor.

**R:** Informe hash e resultado do push. Mensagem sugerida:
`feat: implementar pipeline backend RAG`.

------------------------------------------------------------------------

# CAP04 --- IMPLEMENTAÇÃO DO FRONT-END

## Prompt 27 --- Criar frontend Streamlit mínimo

**C:** O backend já expõe uma operação de pergunta e resposta.

**O:** Crie uma interface Streamlit mínima com título, identificação do
manual, campo de pergunta, botão/entrada de envio, área de resposta,
fontes e mensagens de erro.

**S:** Interface funcional e simples; não priorize estética.

**T:** Claro e amigável.

**A:** Usuário não técnico consultando o manual.

**R:** Implemente sem duplicar lógica do RAG no frontend.

------------------------------------------------------------------------

## Prompt 28 --- Integrar frontend ao RAG Service

**C:** A interface existe e o backend está funcional.

**O:** Conecte o Streamlit ao RAG Service. Garanta que uma pergunta
vazia não seja processada e que erros do backend sejam apresentados de
forma compreensível.

**S:** Integração fina.

**T:** Técnico.

**A:** Usuário do MVP.

**R:** Implemente e descreva o fluxo
`UI → RAG Service → resposta/fontes → UI`.

------------------------------------------------------------------------

## Prompt 29 --- Gerenciar inicialização e estado

**C:** Modelos e índice podem ser caros para recarregar a cada interação
do Streamlit.

**O:** Analise a inicialização do modelo de embeddings, índice e demais
recursos. Use mecanismos de cache/estado do Streamlit somente onde
trouxer benefício claro e sem esconder a lógica do RAG.

**S:** Otimização mínima e justificada.

**T:** Técnico.

**A:** Desenvolvedor.

**R:** Antes de alterar, explique o problema observado e a solução
proposta; depois implemente apenas o necessário.

------------------------------------------------------------------------

## Prompt 30 --- Revisão de integração CAP04

**C:** O usuário já consegue perguntar e receber resposta com fontes.

**O:** Revise frontend e integração procurando lógica duplicada, erros
não tratados, estado inconsistente, recarregamentos caros e dependência
excessiva da UI.

**S:** Integration review.

**T:** Crítico e construtivo.

**A:** Desenvolvedor.

**R:** Checklist por severidade; não altere código sem aprovação.

------------------------------------------------------------------------

## Prompt 31 --- Consolidar e versionar CAP04

**C:** Ajustes aprovados foram concluídos.

**O:** Execute um fluxo manual de demonstração, crie um conventional
commit e faça push para `origin`.

**S:** Fechamento de etapa.

**T:** Objetivo.

**A:** Desenvolvedor.

**R:** Informe hash e resultado do push. Mensagem sugerida:
`feat: integrar interface Streamlit ao RAG`.

------------------------------------------------------------------------

# CAP05 --- TESTES E QUALIDADE

## Prompt 32 --- Planejar estratégia de testes

**C:** O MVP funcional está implementado.

**O:** Mapeie testes unitários, integração e avaliação de RAG
necessários para os requisitos definidos no CAP02. Priorize risco e
valor.

**S:** Estratégia enxuta.

**T:** Analítico.

**A:** Desenvolvedor/testador.

**R:** Atualize documentação de testes com matriz
`requisito → teste → tipo → prioridade`.

------------------------------------------------------------------------

## Prompt 33 --- Testar PDF Loader e Chunker

**C:** Precisamos validar a ingestão independentemente do modelo.

**O:** Crie testes pytest para arquivo inexistente, PDF válido,
documento sem texto quando viável, chunking, overlap e preservação de
metadados.

**S:** Testes determinísticos e pequenos.

**T:** Técnico.

**A:** Desenvolvedor.

**R:** Implemente e execute os testes, mostrando resumo.

------------------------------------------------------------------------

## Prompt 34 --- Testar embeddings, Vector Store e Retriever

**C:** Componentes de recuperação precisam ser verificados sem depender
do LLM sempre que possível.

**O:** Crie testes para dimensões/quantidade de embeddings, indexação,
Top-K e retrieval. Use mocks/fakes quando isso tornar o teste mais
determinístico e rápido.

**S:** Testes focados em contrato e comportamento.

**T:** Técnico.

**A:** Desenvolvedor.

**R:** Implemente, execute e identifique claramente testes que dependem
de modelo externo.

------------------------------------------------------------------------

## Prompt 35 --- Testar Prompt Builder e RAG Service

**C:** Precisamos validar composição do contexto e orquestração.

**O:** Teste pergunta vazia, contexto disponível, contexto insuficiente,
preservação de fontes e tratamento de falha do LLM. Evite testar texto
exato de resposta generativa quando isso for frágil.

**S:** Testes robustos e orientados a invariantes.

**T:** Técnico.

**A:** Desenvolvedor.

**R:** Implemente e execute.

------------------------------------------------------------------------

## Prompt 36 --- Criar conjunto de avaliação RAG

**C:** Testes de software não garantem qualidade da resposta.

**O:** Crie um pequeno conjunto de avaliação com perguntas sobre o
manual: respostas presentes, perguntas ambíguas e perguntas fora do
conteúdo. Registre resposta esperada ou evidência esperada e páginas
relevantes.

**S:** Dataset manual pequeno e auditável.

**T:** Analítico.

**A:** Desenvolvedor avaliando retrieval e grounding.

**R:** Salve em formato simples dentro de `tests/` ou `docs/`, com
justificativa da escolha.

------------------------------------------------------------------------

## Prompt 37 --- Avaliar retrieval e respostas

**C:** O conjunto de avaliação foi criado.

**O:** Execute a avaliação usando `gemma3:4b` como baseline fixo e
separe os resultados em: retrieval correto/incorreto, contexto
suficiente/insuficiente, resposta fundamentada/não fundamentada e recusa
adequada/inadequada. Não troque automaticamente o LLM para corrigir
falhas; primeiro identifique em qual etapa do RAG a falha ocorreu.

**S:** Avaliação transparente; não esconda resultados ruins.

**T:** Investigativo.

**A:** Desenvolvedor estudando qualidade de RAG.

**R:** Produza relatório resumido com casos de falha e hipóteses de
causa. Não ajuste parâmetros automaticamente.

------------------------------------------------------------------------

## Prompt 38 --- Revisão DRY/SRP e qualidade

**C:** Temos código e testes.

**O:** Revise DRY, SRP, nomes, tamanho de funções, acoplamento,
duplicação, tratamento de erros e testabilidade. Só proponha
refatorações que reduzam risco ou melhorem clareza.

**S:** Refatoração conservadora.

**T:** Crítico.

**A:** Desenvolvedor.

**R:** Liste propostas com benefício, risco e arquivos afetados antes de
implementar.

------------------------------------------------------------------------

## Prompt 39 --- Executar suíte e cobertura

**C:** As refatorações aprovadas foram concluídas.

**O:** Execute toda a suíte. Se houver ferramenta de cobertura já
prevista no projeto, reporte cobertura por módulo; não persiga 100%
artificialmente.

**S:** Quality gate.

**T:** Objetivo.

**A:** Desenvolvedor.

**R:** Informe testes aprovados/falhos, cobertura relevante e riscos
residuais.

------------------------------------------------------------------------

## Prompt 40 --- Consolidar e versionar CAP05

**C:** Testes e avaliação estão concluídos.

**O:** Verifique documentação de qualidade, testes e Git. Crie um
conventional commit e faça push para `origin`.

**S:** Fechamento de etapa.

**T:** Objetivo.

**A:** Desenvolvedor.

**R:** Informe hash e resultado do push. Mensagem sugerida:
`test: adicionar testes e avaliação do RAG`.

------------------------------------------------------------------------

# CAP06 --- ENTREGA FINAL

## Prompt 41 --- Atualizar README final

**C:** O MVP está funcional e testado.

**O:** Transforme o README em guia completo e fiel ao sistema
implementado: objetivo, arquitetura, stack, requisitos, instalação,
configuração do Ollama/modelo, incluindo `gemma3:4b` como baseline
validado localmente, PDF, execução, testes, pipeline RAG, limitações e
troubleshooting básico. Inclua comandos de verificação como
`ollama list` e `ollama ps` somente se forem coerentes com a
implementação final.

**S:** Documentação reproduzível.

**T:** Profissional e didático.

**A:** Pessoa que recebe o repositório sem contexto prévio.

**R:** Atualize somente com comandos e funcionalidades realmente
existentes.

------------------------------------------------------------------------

## Prompt 42 --- Criar roteiro de demonstração

**C:** Precisamos demonstrar o MVP de forma repetível.

**O:** Crie um roteiro curto de demo com inicialização, indexação de
`data/guia-pratico-engenharia-software-com-ia-generativa.pdf` quando
aplicável e 5--10 perguntas representativas, incluindo pelo menos uma
pergunta fora do conteúdo do manual.

**S:** Demonstração prática.

**T:** Claro.

**A:** Professor/revisor técnico.

**R:** Salve em `docs/demo.md`.

------------------------------------------------------------------------

## Prompt 43 --- Criar checklist de release

**C:** O projeto está próximo da entrega.

**O:** Crie checklist final cobrindo ambiente reproduzível,
dependências, `.env.example`, PDF de demonstração, testes, aplicação,
fontes, README, arquitetura, limitações, segurança básica e Git limpo.

**S:** Checklist operacional.

**T:** Objetivo.

**A:** Desenvolvedor responsável pela entrega.

**R:** Salve em `docs/release-checklist.md`.

------------------------------------------------------------------------

## Prompt 44 --- Revisão técnica final profunda

**C:** Este é o gate final do Lab03. O sistema deve continuar sendo um
MVP educacional, não uma aplicação de produção.

**O:** Faça revisão técnica completa sem alterar código. Analise
arquitetura, separação de responsabilidades, segurança, dependências,
testes, configuração, erros, pipeline RAG, retrieval, grounding, fontes,
documentação e reprodutibilidade.

**S:** Revisão profunda baseada em evidências do repositório.

**T:** Crítico, preciso e construtivo.

**A:** Desenvolvedor e avaliador do laboratório.

**R:** Classifique achados em `Bloqueador`, `Alto`, `Médio`, `Baixo` e
`Evolução futura`. Para cada achado, informe evidência, impacto e ação
recomendada. Não confunda melhorias futuras com defeitos do MVP.

------------------------------------------------------------------------

## Prompt 45 --- Corrigir somente achados aprovados

**C:** A revisão final gerou uma lista de achados. Apenas itens
explicitamente aprovados devem ser modificados.

**O:** Implemente as correções aprovadas uma a uma, mantendo o escopo.
Após cada grupo de mudanças, execute os testes relacionados.

**S:** Mudanças pequenas e rastreáveis.

**T:** Técnico.

**A:** Desenvolvedor.

**R:** Para cada correção: achado → arquivos alterados → solução →
testes executados → resultado.

------------------------------------------------------------------------

## Prompt 46 --- Validação final

**C:** As correções finais foram concluídas.

**O:** Execute a validação final do projeto: testes, smoke test do
chatbot, pergunta com resposta, pergunta sem resposta, fontes, comandos
do README e estado do Git.

**S:** Release validation.

**T:** Objetivo.

**A:** Responsável pela entrega.

**R:** Preencha o checklist de release com evidências e destaque
qualquer item ainda pendente.

------------------------------------------------------------------------

## Prompt 47 --- Commit final

**C:** O checklist de release está aprovado.

**O:** Mostre `git status`, resumo das mudanças finais, crie um
conventional commit de entrega e faça push para `origin`. A autorização
para esse push já foi dada na conversa do projeto.

**S:** Encerramento controlado.

**T:** Conciso.

**A:** Desenvolvedor.

**R:** Informe arquivos incluídos, hash, branch e resultado do push.
Mensagem sugerida: `docs: finalizar entrega do MVP RAG`.

------------------------------------------------------------------------

# Gates entre capítulos

Não avançar automaticamente de capítulo. Ao final de cada CAP: 1.
executar revisão; 2. analisar achados; 3. corrigir somente o que for
aprovado; 4. executar testes/verificações aplicáveis; 5. revisar
`git status`; 6. criar conventional commit; 7. fazer push para `origin`;
8. iniciar o capítulo seguinte somente após confirmação.

# Regra de ouro para o Codex

Sempre preferir a menor mudança que satisfaça o requisito atual. Não
antecipar funcionalidades de capítulos posteriores.
