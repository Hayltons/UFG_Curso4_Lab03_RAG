# Frontend Streamlit — verificação do CAP04

`streamlit_app.py` apresenta o nome do manual, formulário de pergunta, resposta e páginas consultadas. Ele chama `RAGService` para ingestão e consulta; não implementa embeddings, busca, prompt ou chamada ao LLM. Perguntas vazias são rejeitadas antes de `ask()`; erros conhecidos aparecem como mensagens na tela, sem traceback. Páginas repetidas de chunks diferentes são exibidas uma vez, com o rótulo **Fontes consultadas**.

## Inicialização e estado

Interações do Streamlit reexecutam o script. Sem estado, cada envio carregaria o modelo de embeddings e indexaria o PDF novamente. O serviço fica em `st.session_state`, isolado por sessão. Sua assinatura inclui a configuração efetiva, tamanho e horário de modificação do PDF; uma mudança recria o serviço e limpa a resposta anterior. O `.env` é relido a cada chamada de configuração, preservando a precedência das variáveis do processo. Cada nova sessão carrega seu próprio modelo/índice, escolha simples para o MVP local que evita compartilhar um objeto mutável global.

## Verificação executada

- Python 3.11.6, Streamlit 1.65.0, `pip check` sem conflitos e `compileall` sem erros.
- `AppTest` abriu a tela com título, campo e botão, sem exceções; o serviço foi indexado na sessão.
- Envio vazio mostrou “Digite uma pergunta antes de enviar.” e não guardou resposta.
- Pergunta sobre diagnóstico de resposta RAG incorreta recebeu a explicação do manual com citação da página 12; a interface exibiu fontes consultadas.
- Pergunta sobre o preço atual do Bitcoin recebeu “Não encontrei essa informação no manual consultado.”
- O mesmo objeto de serviço foi reutilizado entre perguntas. Alterar `TOP_K` de 4 para 3 provocou nova indexação, sem exceções.
- URL local inválida do Ollama mostrou erro legível na interface; PDF ausente mostrou erro de inicialização e impediu o formulário. Nenhum caso exibiu exceção do Streamlit.
- O servidor real iniciou em `127.0.0.1:8509` e respondeu `200 ok` em `/_stcore/health`; foi encerrado após a verificação.

## Revisão de integração

- **Crítico/Importante:** nenhum defeito observado nos fluxos exercitados. Não há lógica de RAG duplicada na interface, e uma pergunta não reindexa o documento.
- **Baixo — `streamlit_app.py`, `ready_service()`:** cada sessão ocupa memória própria para modelo e índice. Para o MVP local isso evita o requisito de segurança de acesso concorrente de um cache global; se houver muitas sessões, medir consumo e avaliar compartilhamento seguro antes de mudar a estratégia.
- **Qualidade a avaliar no CAP05:** fontes consultadas não são prova de que cada trecho sustenta a resposta. A interface explicita essa limitação; a consistência da fundamentação e da recusa exige mais casos.

A suíte pytest e a avaliação ampla de qualidade permanecem no CAP05.
