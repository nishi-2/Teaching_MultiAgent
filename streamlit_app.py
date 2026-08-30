import logging

import streamlit as st

from app.agents.gpt_teaching_agent import GPTTeachingAgent
from app.agents.pdf_rag_agent import PDFRAGAgent
from app.config.logging_config import configure_logging
from app.config.settings import settings
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest
from app.ingestion.indexer import DocumentIndexer
from app.ingestion.manifest import IngestionManifest
from app.retrieval.openai_embeddings import OpenAIEmbeddingProvider
from app.retrieval.qdrant_store import QdrantStore
from app.ui.document_manager import save_uploaded_pdf
from app.ingestion.manifest import IngestionManifest



configure_logging(settings.log_level)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Teaching Tutor",
    page_icon="AI",
    layout="centered",
)

if "active_document_id" not in st.session_state:
    st.session_state.active_document_id = None


@st.cache_resource
def get_coordinator() -> Coordinator:
    teaching_agent = GPTTeachingAgent(settings=settings)
    pdf_rag_agent = PDFRAGAgent(settings=settings)
    return Coordinator(
        teaching_agent=teaching_agent,
        pdf_rag_agent=pdf_rag_agent,
    )


@st.cache_resource
def get_indexer() -> DocumentIndexer:
    embedder = OpenAIEmbeddingProvider(settings=settings)
    store = QdrantStore(settings=settings)
    manifest = IngestionManifest()
    return DocumentIndexer(
        embedder=embedder,
        store=store,
        manifest=manifest,
    )


st.title("AI Teaching Tutor")
st.caption("Phase 4: Streamlit → Coordinator → GPT + PDF RAG")

with st.sidebar:
    st.header("Settings")
    learner_level = st.selectbox(
        "Learner level",
        options=["beginner", "intermediate", "advanced"],
    )
    st.write(f"Model: `{settings.openai_model}`")
    st.write(f"Embedding model: `{settings.openai_embedding_model}`")

    st.header("PDF documents")
    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
    )

    if uploaded_file is not None and st.button("Save and index PDF"):
        try:
            saved_path = save_uploaded_pdf(
                uploaded_file,
                documents_dir=settings.documents_dir,
            )
            record = get_indexer().index_file(saved_path)
        except Exception:
            logger.exception("PDF indexing failed")
            st.error("The PDF could not be indexed.")
        else:
            if record.status == "indexed":
                st.session_state.active_document_id = record.document_id
                st.success(
                    f"Indexed {record.file_name}: "
                    f"{record.page_count} pages, "
                    f"{record.chunk_count} chunks."
                )
            else:
                st.error(record.error_message or "PDF indexing failed.")

        st.header("Indexed documents")
    documents = IngestionManifest().list_documents()


    if not documents:
        st.caption("No documents have been indexed yet.")
    else:
        for document in documents:
            st.write(
                f"**{document.file_name}** — "
                f"{document.status}, "
                f"{document.page_count or 0} pages, "
                f"{document.chunk_count} chunks"
            )


question = st.text_area(
    "What would you like to learn?",
    placeholder="For example: Explain the topic in my uploaded PDF.",
)

if st.button("Ask Tutor", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        logger.info("Received tutor question")
        request = TutorRequest(
            question=question,
            learner_level=learner_level,
            active_document_id=st.session_state.active_document_id,
        )

        try:
            response = get_coordinator().handle_request(request)
        except Exception:
            logger.exception("Tutor request failed")
            st.error("The tutor could not complete the request.")
        else:
            if response.status == "success":
                st.subheader("Tutor response")
                st.write(response.answer)
            else:
                st.error(response.answer)
