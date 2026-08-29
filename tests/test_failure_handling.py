from app.agents.base import BaseSubagent
from app.coordinator.coordinator import Coordinator
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult, TutorRequest


class FailingTeachingAgent(BaseSubagent):
    name = "teaching_agent"

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="failed",
            metadata={"error": "Simulated agent failure"},
        )


def test_coordinator_handles_agent_failure() -> None:
    coordinator = Coordinator(teaching_agent=FailingTeachingAgent())
    response = coordinator.handle_request(
        TutorRequest(question="What is Python?")
    )

    assert response.status == "failed"
    assert "could not complete" in response.answer.lower()
