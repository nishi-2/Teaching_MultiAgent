from typing import List

from app.agents.pdf_rag_agent import PDFRAGAgent
from app.config.settings import Settings
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult


class FakeEmbedder:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2]]


class FilteringStore:
    def __init__(self):
        self.received_document_id = None

    def search_vectors(self, query_vector, limit, document_id=None):
        self.received_document_id = document_id
        return [
            {
                "id": "selected-document-point",
                "score": 0.95,
                "payload": {
                    "document_id": "new-document",
                    "file_name": "new.pdf",
                    "page_number": 1,
                    "text": "Evidence from the selected document.",
                },
            }
        ]


class FakeCoordinator(CoordinatorGateway):
    def __init__(self):
        self.findings = []

    def submit_finding(self, task_id: str, finding: str) -> None:
        self.findings.append(finding)

    def request_context(self, task_id: str, topic: str) -> List[str]:
        return []

    def request_follow_up(
        self,
        task: CoordinatorTask,
        objective: str,
    ) -> SubagentResult:
        return SubagentResult(
            task_id=task.task_id,
            agent_name=task.assigned_agent,
            status="partial",
        )


def test_pdf_agent_filters_to_active_document() -> None:
    store = FilteringStore()
    agent = PDFRAGAgent(
        settings=Settings(retrieval_score_threshold=0.20),
        embedder=FakeEmbedder(),
        store=store,
    )
    coordinator = FakeCoordinator()
    task = CoordinatorTask(
        task_id="task-1",
        parent_request_id="request-1",
        assigned_agent="pdf_rag_agent",
        objective="Retrieve selected PDF evidence",
        user_question="Explain the selected PDF.",
        approved_context={"active_document_id": "new-document"},
    )

    result = agent.run(task, coordinator)

    assert result.status == "success"
    assert store.received_document_id == "new-document"
    assert "new.pdf" in coordinator.findings[0]
