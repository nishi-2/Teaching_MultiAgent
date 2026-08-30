from typing import List

from app.agents.pdf_rag_agent import PDFRAGAgent
from app.config.settings import Settings
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult


class FakeEmbedder:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2]]


class FakeStore:
    def search_vectors(self, query_vector, limit, document_id=None):
        return [
            {
                "id": "weak-match",
                "score": 0.10,
                "payload": {
                    "document_id": "document-1",
                    "file_name": "sample.pdf",
                    "page_number": 1,
                    "text": "Weak evidence",
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


def test_pdf_agent_rejects_weak_matches() -> None:
    settings = Settings(retrieval_score_threshold=0.20)
    agent = PDFRAGAgent(
        settings=settings,
        embedder=FakeEmbedder(),
        store=FakeStore(),
    )
    coordinator = FakeCoordinator()
    task = CoordinatorTask(
        task_id="task-1",
        parent_request_id="request-1",
        assigned_agent="pdf_rag_agent",
        objective="Retrieve PDF evidence",
        user_question="Explain the document.",
    )

    result = agent.run(task, coordinator)

    assert result.status == "partial"
    assert result.metadata["match_count"] == 0
    assert "No sufficiently relevant" in coordinator.findings[0]
