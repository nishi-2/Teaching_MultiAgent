from typing import Optional

from app.agents.base import BaseSubagent
from app.config.settings import Settings
from app.coordinator.gateway import CoordinatorGateway
from app.domain.evidence import PDFEvidence
from app.domain.messages import CoordinatorTask, SubagentResult
from app.retrieval.embeddings import EmbeddingProvider
from app.retrieval.openai_embeddings import OpenAIEmbeddingProvider
from app.retrieval.qdrant_store import QdrantStore


class PDFRAGAgent(BaseSubagent):
    name = "pdf_rag_agent"

    def __init__(
        self,
        settings: Settings,
        embedder: Optional[EmbeddingProvider] = None,
        store: Optional[QdrantStore] = None,
    ) -> None:
        self.settings = settings
        self.embedder = embedder or OpenAIEmbeddingProvider(settings=settings)
        self.store = store or QdrantStore(settings=settings)

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        query_vector = self.embedder.embed_texts(
            [task.user_question]
        )[0]
        active_document_id = task.approved_context.get(
            "active_document_id"
        )

        raw_matches = self.store.search_vectors(
            query_vector=query_vector,
            limit=5,
            document_id=active_document_id,
        )

        matches = [
            match
            for match in raw_matches
            if float(match["score"]) >= self.settings.retrieval_score_threshold
        ]

        if not matches:
            coordinator.submit_finding(
                task_id=task.task_id,
                finding="No sufficiently relevant PDF evidence was found.",
            )
            return SubagentResult(
                task_id=task.task_id,
                agent_name=self.name,
                status="partial",
                metadata={
                    "match_count": 0,
                    "threshold": self.settings.retrieval_score_threshold,
                },
            )

        for match in matches:
            payload = match["payload"]
            evidence = PDFEvidence(
                document_id=str(payload.get("document_id", "unknown")),
                file_name=str(payload.get("file_name", "unknown")),
                page_number=int(payload.get("page_number", 1)),
                excerpt=str(payload.get("text", "")),
                similarity_score=float(match["score"]),
            )
            finding = (
                f"PDF source: {evidence.citation_label()} | "
                f"similarity {evidence.similarity_score:.4f}\n"
                f"{evidence.excerpt}"
            )
            coordinator.submit_finding(
                task_id=task.task_id,
                finding=finding,
            )

        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            metadata={
                "match_count": len(matches),
                "threshold": self.settings.retrieval_score_threshold,
            },
        )
