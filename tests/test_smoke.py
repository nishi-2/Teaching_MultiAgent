from app.agents.teaching_agent import TeachingAgent
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest


def test_coordinator_returns_teaching_response() -> None:
    coordinator = Coordinator(teaching_agent=TeachingAgent())
    request = TutorRequest(question="What is Python?")
    response = coordinator.handle_request(request)

    assert response.status == "success"
    assert "python" in response.answer.lower()
