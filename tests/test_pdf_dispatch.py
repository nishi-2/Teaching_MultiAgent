from app.agents.teaching_agent import TeachingAgent
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest


def test_coordinator_dispatches_pdf_agent() -> None:
    coordinator = Coordinator(teaching_agent=TeachingAgent())
    response = coordinator.handle_request(
        TutorRequest(
            question="Teach me from my uploaded PDF document."
        )
    )

    assert response.status == "success"
    assert "Teaching plan created" in response.answer
    assert "PDF RAG Agent received" in response.answer
