from app.agents.teaching_agent import TeachingAgent
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest


def test_coordinator_dispatches_multiple_agents() -> None:
    coordinator = Coordinator(teaching_agent=TeachingAgent())
    response = coordinator.handle_request(
        TutorRequest(
            question="Find the latest GitHub repository code example."
        )
    )

    assert response.status == "success"
    assert "Teaching plan created" in response.answer
    assert "Web Research Agent received" in response.answer
    assert "GitHub Agent received" in response.answer
