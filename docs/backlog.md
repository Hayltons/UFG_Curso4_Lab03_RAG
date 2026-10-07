# Backlog incremental do MVP

As tarefas seguem a ordem CAP03 → CAP06. Cada item deve produzir uma mudança pequena e verificável; os critérios detalhados estão em [requisitos.md](requisitos.md). Dependências são IDs desta tabela.

| ID | Capítulo | Tarefa | Depende de | Critério de pronto |
| --- | --- | --- | --- | --- |
| B01 | CAP03 | Centralizar e validar configuração do PDF, modelos, chunking, Top-K e contexto. | — | Parâmetros inválidos e caminho ausente geram diagnóstico claro; `gemma3:4b` é o padrão generativo. |
| B02 | CAP03 | Extrair texto por página com PyMuPDF. | B01 | PDF do MVP gera páginas com origem e número; ausente, inválido ou sem texto é tratado. |
| B03 | CAP03 | Dividir páginas em trechos com sobreposição. | B02 | Trechos não cruzam páginas, preservam metadados e respeitam parâmetros válidos. |
| B04 | CAP03 | Gerar embeddings de trechos e perguntas. | B01, B03 | Quantidade e dimensão são consistentes; truncamento do modelo é verificado no PDF. |
| B05 | CAP03 | Indexar vetores normalizados no FAISS. | B04 | Índice e lista de trechos permanecem alinhados; consulta Top-K devolve score e origem. |
| B06 | CAP03 | Recuperar trechos para uma pergunta sem chamar LLM. | B04, B05 | Retriever devolve resultados ordenados, com limite K e metadados. |
| B07 | CAP03 | Construir prompt com contexto limitado e referências. | B06 | Prompt inclui pergunta, trechos e instrução de não inventar; contexto vazio tem tratamento claro. |
| B08 | CAP03 | Conectar ao Ollama por HTTP. | B01 | Cliente retorna texto de `gemma3:4b` e relata serviço/modelo indisponível. |
| B09 | CAP03 | Orquestrar `ingest` e `ask` no RAG Service. | B02–B08 | Python consulta o índice sem Streamlit e devolve resposta mais fontes. |
| B10 | CAP03 | Executar smoke test do backend. | B09 | Uma pergunta coberta e outra fora do manual registram trechos, páginas, resposta e etapa de eventual falha. |
| B11 | CAP04 | Criar interface Streamlit e integrá-la somente ao serviço. | B09 | Usuário pergunta e vê resposta, fontes e erros; entrada vazia não é processada. |
| B12 | CAP04 | Ajustar inicialização e cache de recursos, se necessário. | B11 | Perguntas repetidas não reindexam o PDF; a escolha de cache é explicada e verificada. |
| B12A | CAP04 | Substituir o fluxo textual da seção Arquitetura do README por um diagrama Mermaid. | B11, B12 | Diagrama reflete a interface e os fluxos reais de ingestão e consulta; é revisado após a integração e antes do commit e push do CAP04. |
| B13 | CAP05 | Mapear testes contra RF/RNF e priorizar riscos. | B09, B11 | Matriz requisito → teste → tipo → prioridade está documentada. |
| B14 | CAP05 | Testar Loader e Chunker. | B02, B03, B13 | Casos de PDF válido/ausente/inválido/sem texto e preservação de páginas, tamanho e overlap passam. |
| B15 | CAP05 | Testar embeddings, índice e Retriever. | B04–B06, B13 | Vetores, Top-K, scores e metadados passam em testes determinísticos quando possível. |
| B16 | CAP05 | Testar Prompt Builder, cliente e RAG Service. | B07–B09, B13 | Pergunta vazia, contexto, fontes, recusa sem trechos e falhas do Ollama são cobertos. |
| B17 | CAP05 | Criar casos de avaliação a partir do PDF. | B10 | Há perguntas explícitas, distribuídas, ambíguas e fora do manual com evidência/página esperadas. |
| B18 | CAP05 | Avaliar retrieval e geração com `gemma3:4b`. | B17 | Relatório separa recuperação, suficiência do contexto, fundamentação, fontes e recusa; falhas são registradas. |
| B19 | CAP05 | Revisar qualidade e executar suíte. | B14–B18 | Ajustes justificados são verificados; testes e limitações residuais são informados. |
| B20 | CAP06 | Atualizar README e documentação conforme o sistema real. | B19 | Instalação, configuração, execução, testes, arquitetura, limites e solução de problemas foram exercitados. |
| B21 | CAP06 | Criar roteiro de demonstração e checklist. | B18, B20 | Demo inclui perguntas com e sem resposta; checklist registra evidências. |
| B22 | CAP06 | Validar entrega, revisar e versionar. | B20, B21 | Testes, smoke test, README, PDF, fontes e estado do Git foram conferidos; commit e push publicados. |

O fechamento de cada capítulo inclui revisão, verificações aplicáveis, conventional commit e push para `origin`. Nenhuma tarefa deste backlog antecipa implementação no CAP02.
