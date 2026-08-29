from app.agents.base import BaseSubagent
from app.coordinator.coordinator import Coordinator
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult, TutorRequest


class ContextAwareAgent(BaseSubagent):
    name = "teaching_agent"

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        coordinator.submit_finding(
            task_id=task.task_id,
            finding="Python is a programming language.",
        )

        approved_context = coordinator.request_context(
            task_id=task.task_id,
            topic="python",
        )

        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            findings=[
                f"Coordinator returned context: {approved_context}"
            ],
        )


def test_subagent_uses_coordinator_for_context() -> None:
    coordinator = Coordinator(teaching_agent=ContextAwareAgent())
    response = coordinator.handle_request(
        TutorRequest(question="Teach me Python.")
    )

    assert response.status == "success"
    assert "Python is a programming language." in response.answer
    assert "Coordinator returned context" in response.answer
