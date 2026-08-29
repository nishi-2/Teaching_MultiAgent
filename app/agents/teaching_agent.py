from app.agents.base import BaseSubagent
from app.domain.messages import CoordinatorTask, SubagentResult


class TeachingAgent(BaseSubagent):
    name = "teaching_agent"

    def run(self, task: CoordinatorTask) -> SubagentResult:
        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            findings=[
                f"Teaching plan created for: {task.user_question}"
            ],
        )