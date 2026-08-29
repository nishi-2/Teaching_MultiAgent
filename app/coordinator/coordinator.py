from uuid import uuid4
from typing import Dict, List

from app.agents.base import BaseSubagent
from app.domain.messages import CoordinatorTask, SubagentResult, TutorRequest, TutorResponse

from app.coordinator.context_store import CoordinatorContextStore
from app.coordinator.gateway import CoordinatorGateway
from app.coordinator.router import CoordinatorRouter


class Coordinator(CoordinatorGateway):
    def __init__(self, teaching_agent: BaseSubagent) -> None:
        self.agents: Dict[str, BaseSubagent] = {
            "teaching_agent": teaching_agent,
        }
        self.router = CoordinatorRouter()
        self.context_store = CoordinatorContextStore()
        self._task_to_request: Dict[str, str] = {}


    def submit_finding(self, task_id: str, finding: str) -> None:
        """ Store a subagent finding under its parent request """
        request_id = self._task_to_request.get(task_id)
        if request_id is not None:
            self.context_store.add_finding(request_id, finding)


    def request_context(self, task_id: str, topic: str) -> list[str]:
        """Return approved findings for a subagent task."""
        request_id = self._task_to_request.get(task_id)

        if request_id is None:
            return []

        return self.context_store.search_findings(request_id, topic)


    def request_follow_up(self, task: CoordinatorTask, objective: str,) -> SubagentResult:
        """Return a controlled response until follow-up routing is implemented."""
        return SubagentResult(
            task_id=task.task_id,
            agent_name=task.assigned_agent,
            status="partial",
            findings=[],
            follow_up_objective=objective,
            metadata={"message": "Follow-up routing will be implemented next."},
        )

    def dispatch(self, task: CoordinatorTask) -> SubagentResult:
        """Dispatch one task to one registered subagent."""
        agent = self.agents.get(task.assigned_agent)

        if agent is None:
            return SubagentResult(
                task_id=task.task_id,
                agent_name=task.assigned_agent,
                status="failed",
                findings=[],
                metadata={"error": "Agent is not registered."},
            )

        return agent.run(task, coordinator=self)


    def handle_request(self, request: TutorRequest) -> TutorResponse:
        parent_request_id = str(uuid4())
        selected_agents = self.router.select_agents(request.question)
        results: List[SubagentResult] = []

        for agent_name in selected_agents:
            if agent_name not in self.agents:
                continue

            task = CoordinatorTask(
                task_id=str(uuid4()),
                parent_request_id=parent_request_id,
                assigned_agent=agent_name,
                objective="Process the user question",
                user_question=request.question,
            )

            self._task_to_request[task.task_id] = parent_request_id
            result = self.dispatch(task)
            results.append(result)

            for finding in result.findings:
                self.submit_finding(task.task_id, finding)

        if not results or all(result.status == "failed" for result in results):
            return TutorResponse(
                answer="The Coordinator could not complete the request.",
                status="failed",
            )

        answer = "\n".join(self.context_store.get_findings(parent_request_id))
        return TutorResponse(answer=answer, status="success")

