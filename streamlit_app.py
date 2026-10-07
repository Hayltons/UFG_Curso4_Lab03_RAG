"""Interface mínima para consultar o manual através do RAGService."""

import logging

import streamlit as st

from app.config import load_config
from app.models import RAGAnswer
from app.rag_service import RAGService, create_service


log = logging.getLogger(__name__)


def ready_service() -> RAGService:
    """Mantém o índice por sessão e o recria quando PDF/configuração mudam."""
    config = load_config()
    try:
        pdf_stat = config.pdf_path.stat()
    except OSError as exc:
        raise FileNotFoundError(f"PDF não encontrado ou inacessível: {config.pdf_path}") from exc
    signature = (config, pdf_stat.st_mtime_ns, pdf_stat.st_size)
    if st.session_state.get("rag_signature") != signature:
        with st.spinner("Preparando o manual para consulta..."):
            service = create_service(config)
            service.ingest()
        st.session_state["rag_service"] = service
        st.session_state["rag_signature"] = signature
        st.session_state.pop("last_answer", None)
    return st.session_state["rag_service"]


def show_answer(result: RAGAnswer) -> None:
    st.subheader("Resposta")
    st.write(result.answer)
    st.subheader("Fontes consultadas")
    st.caption("Trechos enviados ao modelo; a lista não confirma que todos sustentam a resposta.")
    references = dict.fromkeys((item.chunk.source, item.chunk.page) for item in result.sources)
    if references:
        for source, page in references:
            st.write(f"{source} — página {page}")
    else:
        st.write("Nenhum trecho foi enviado ao modelo.")


def main() -> None:
    st.set_page_config(page_title="Lab03 — Chatbot RAG", page_icon="📘")
    st.title("Chatbot RAG — Engenharia de Software com IA Generativa")
    st.caption("Pergunte sobre o manual PDF do Lab03.")

    try:
        service = ready_service()
    except (OSError, ValueError, RuntimeError) as exc:
        st.error(f"Não foi possível preparar o manual: {exc}")
        st.stop()
    except Exception:
        log.exception("Erro inesperado ao preparar o manual")
        st.error("Ocorreu um erro inesperado ao preparar o manual. Consulte o terminal.")
        st.stop()

    st.write(f"**Manual:** {service.config.pdf_path.name}")
    with st.form("question_form"):
        question = st.text_input("Pergunta", placeholder="O que investigar quando uma resposta RAG está errada?")
        submitted = st.form_submit_button("Perguntar")

    if submitted:
        st.session_state.pop("last_answer", None)
        if not question.strip():
            st.warning("Digite uma pergunta antes de enviar.")
        else:
            try:
                with st.spinner("Consultando o manual..."):
                    st.session_state["last_answer"] = service.ask(question.strip())
            except (OSError, ValueError, RuntimeError) as exc:
                st.error(f"Não foi possível responder: {exc}")
            except Exception:
                log.exception("Erro inesperado ao consultar o manual")
                st.error("Ocorreu um erro inesperado ao consultar o manual. Consulte o terminal.")

    if "last_answer" in st.session_state:
        show_answer(st.session_state["last_answer"])


if __name__ == "__main__":
    main()
