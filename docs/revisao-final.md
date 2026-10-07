# Revisão técnica final — CAP06

Revisão em 7 de outubro de 2026, sobre o baseline do CAP05 (`d789300`) e a documentação de entrega. O escopo continua sendo um MVP educacional local, com PDF único. O responsável pelo projeto decidiu explicitamente concluir a entrega e tratar as respostas incompletas posteriormente; elas permanecem visíveis no README, na demonstração e na avaliação original.

## Achados e decisão de entrega

| Severidade | Evidência | Impacto | Ação e situação |
| --- | --- | --- | --- |
| Bloqueador | Nenhum identificado nos fluxos e no escopo exercitados; suíte, backend real e inicialização HTTP funcionaram. | Permite prosseguir com a entrega educacional com as ressalvas abaixo. | Conferir evidências no [checklist](release-checklist.md); não representa garantia de ausência de defeitos. |
| Alto — qualidade conhecida | C01 e C05 recebem evidência incompleta; C03 responde com “commit rel” apesar da continuação no contexto. Ver [avaliação CAP05](avaliacao-rag.md) e observações brutas. | 3/5 respostas cobertas ficaram incompletas na amostra; a aplicação pode apresentar fragmentos como resposta. | Adiado explicitamente pelo responsável para após o MVP. Avaliar limites de chunk, trechos vizinhos e organização do contexto, medindo regressões. |
| Médio — reprodutibilidade | `requirements.txt` fixa dependências diretas; transitivas e revisão do modelo de embeddings não estão integralmente fixadas. Testes usam a `.venv` existente e cache. | Uma instalação futura pode resolver versões distintas; não há evidência de instalação limpa em outra máquina. | Limite documentado; lock e validação em ambiente novo nos próximos passos. |
| Médio — suficiência e orçamento de contexto | `app/prompt_builder.py` limita caracteres, e `app/ollama_client.py` usa o contexto do runtime Ollama; não há orçamento exato de tokens ou checagem automática de fundamentação. | Outra configuração/PDF pode exceder a janela ou produzir resposta sem respaldo. Score Top-K não certifica relevância. | Manter baseline avaliado nesta entrega; ampliar avaliações antes de mudar parâmetros e modelos. |
| Baixo — recursos por sessão | `streamlit_app.py:ready_service()` cria modelo/índice por sessão e invalida por configuração, tamanho e modificação do PDF. | Mais sessões aumentam memória; a assinatura não é hash de conteúdo. | Aceito para uso local com um PDF; medir consumo antes de compartilhar recursos ou persistir índice. |
| Baixo — amplitude dos testes | 27 casos determinísticos e oito perguntas manuais; o conjunto não cobre todos os erros HTTP, PDFs ou ataques possíveis. Não há ferramenta de cobertura prevista. | A suíte verifica os contratos críticos, sem estabelecer qualidade geral ou segurança completa. | Ampliar testes conforme os riscos e novos comportamentos; sem meta artificial de 100%. |
| Evolução futura | Escopo exclui upload, OCR, vários PDFs, autenticação, múltiplos usuários e outros provedores de geração. | Limita os usos a um manual local e ao serviço Ollama configurado. | Itens registrados em [Próximos passos](../README.md#próximos-passos); não são funcionalidades desta entrega. |

## Arquitetura, erros e segurança básica

Loader, chunker, embeddings, vector store, retriever, prompt e cliente Ollama têm responsabilidades separadas. `RAGService` coordena ingestão e consulta; o frontend apresenta resultados e preserva o serviço na sessão. Não foi identificada necessidade de nova camada ou refatoração estrutural para fechar o MVP. O backend não depende de Streamlit.

O índice só é substituído depois de construir vetores válidos. Perguntas vazias são rejeitadas, fontes correspondem aos chunks efetivamente enviados, e erros conhecidos de PDF/configuração/modelo chegam à interface com mensagens compreensíveis. A UI também captura erros inesperados e registra detalhes no terminal. As fontes são descritas como consultadas, sem promessa de comprovar cada frase.

O PDF está versionado e o aplicativo não executa comandos ou código gerados pelo LLM. O prompt orienta tratar o texto recuperado como dado; isso não é uma barreira garantida contra prompt injection. `.env`, `.venv` e caches estão ignorados; não foram observadas credenciais nos arquivos revisados para esta entrega. O README usa bind explícito em `127.0.0.1`, coerente com ausência de autenticação. A revisão é estática e funcional; não houve pentest ou auditoria automatizada de vulnerabilidades das dependências.

## Tratamento dos achados — Prompt 45

Nenhuma correção funcional foi aplicada no CAP06. A decisão do responsável adia os três casos incompletos; os demais itens são limitações ou evoluções registradas. Os ajustes autorizados nesta etapa foram documentais: README de uso, Mermaid em direção `TD`, contribuição da IA, próximos passos, demo, checklist e referências ao estado final. Backend, frontend, parâmetros e observações baseline permanecem como avaliados no CAP05.

As evidências da nova validação operacional estão no [checklist de release](release-checklist.md). Os resultados do CAP05 não foram substituídos pelos dois casos positivos da validação final.
