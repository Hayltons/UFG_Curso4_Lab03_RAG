# Checklist de release — CAP06

Entrega educacional local verificada em 7 de outubro de 2026. As respostas incompletas C01, C03 e C05 foram aceitas como limitações pelo responsável, que determinou tratá-las após o MVP. Veja a [revisão final](revisao-final.md) e os [próximos passos](../README.md#próximos-passos).

## Ambiente e conteúdo

- [x] Python 3.11.6 na `.venv`, pip 26.2.1 e Git 2.45.2.windows.1 conferidos. `py -3.11 --version` funciona no usuário Windows; o launcher não localizou o runtime no usuário isolado da sandbox.
- [x] `python -m pip install -r requirements.txt` conferiu todas as dependências já instaladas, com índice de rede desativado; `python -m pip check` não encontrou conflitos.
- [x] `.env.example` corresponde à configuração: PDF do MVP, MiniLM multilíngue, `gemma3:4b`, Top-K 4, chunk 350/50 e contexto 2500 caracteres. `.env` é opcional; precedência é processo → arquivo → defaults.
- [x] Ollama 0.34.3 ativo e `gemma3:4b` instalado (`a2af6cc3eb7f`). Depois da consulta, `ollama ps` mostrou `100% GPU` e contexto 4096 no equipamento de referência.
- [x] PDF versionado e extraível: 21 páginas com texto. SHA-256: `57bb2faa2070ac4f1c29bb93b8d6d4c630e70635c7ac348247d6505535097894`.
- [x] Limite de reprodução documentado: uso da `.venv` e cache existentes; não houve instalação limpa em outra máquina nem novo download do modelo. `ollama pull` e `ollama serve` foram conferidos via ajuda, sem baixar/iniciar outro serviço desnecessariamente.

## Testes e execução

- [x] `.\.venv\Scripts\python.exe -m pytest -q`: **27 aprovados em 34,11 s**. Não há ferramenta de cobertura prevista; percentual não medido.
- [x] `.\.venv\Scripts\python.exe -m app.smoke_backend`: ingestão com **59 chunks**, vetores de **384 dimensões** e **zero chunks truncados**.
- [x] Pergunta coberta C02: primeiro chunk na p. 12, score 0,635; resposta orientou verificar retrieval antes de investigar prompt/geração e citou p. 12. Fontes consultadas: 12, 12, 2 e 13.
- [x] Pergunta fora do conteúdo N01: declarou “Não encontrei essa informação no manual consultado.”; nenhum preço inventado. Fontes consultadas: 2, 9, 20 e 19.
- [x] Interface via `AppTest` com backend/Ollama reais: envio vazio gerou aviso; C02 respondeu com citação p. 12; N01 recusou; fontes únicas renderizadas e o mesmo serviço reutilizado, sem exceções. Uma primeira tentativa do script auxiliar falhou na comparação de texto acentuado via PowerShell; a repetição com literais Unicode preservados passou, sem alteração na aplicação.
- [x] Servidor Streamlit real em `127.0.0.1:8509`: `/_stcore/health` retornou `200 ok`; `/` retornou `200` com HTML. Processo de verificação encerrado.
- [x] Avaliação de oito perguntas do CAP05 preservada, inclusive os três resultados incompletos. O CAP06 repetiu o smoke operacional; não recalculou métricas gerais de qualidade.

## Documentação, segurança e Git

- [x] README inclui instalação, configuração, execução, testes, stack, roadmap, Mermaid `TD`, limitações, contribuição da IA e próximos passos.
- [x] [Demo](demo.md) contém oito perguntas com evidências esperadas e identifica os casos incompletos. [Revisão final](revisao-final.md) classifica achados e registra o aceite.
- [x] Uso local em loopback, PDF fixo, prompt trata contexto como dado; revisão não encontrou execução de conteúdo do LLM ou credenciais nos arquivos preparados. `.env`, `.venv` e caches ignorados pelo Git.
- [x] Links locais e âncoras conferidos; README usa Mermaid `TD`. `git diff --check` sem erros; a mudança do diagrama mantém a estrutura existente, sem renderização automatizada.
- [x] Fechamento com conventional commit `docs: finalizar entrega do MVP RAG`, push para `origin/main` e conferência de árvore limpa e igualdade entre `HEAD` e `origin/main`. O hash de entrega fica no histórico Git e no resultado comunicado ao responsável.

Os comandos de clonagem, criação de uma nova `.venv` e download inicial são instruções para um ambiente novo; não foram repetidos sobre este workspace existente. A interface é exercitada por `AppTest` e o servidor HTTP separadamente; não há automação de navegador ou certificação visual nesta validação.
