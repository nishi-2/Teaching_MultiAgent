from app.agents.base import BaseSubagent
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult


class TeachingAgent(BaseSubagent):
    name = "teaching_agent"

    def run(self, task: CoordinatorTask, coordinator: CoordinatorGateway,) -> SubagentResult:
        finding = f"Teaching plan created for: {task.user_question}"

        coordinator.submit_finding(task_id=task.task_id, finding=finding,)

        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            findings=[],
        )
