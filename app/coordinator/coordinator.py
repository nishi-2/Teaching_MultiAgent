from typing import Dict, List, Optional
from uuid import uuid4

from app.agents.base import BaseSubagent
from app.agents.stub_agents import GithubAgent, PdfRagAgent, WebResearchAgent
from app.coordinator.context_store import CoordinatorContextStore
from app.coordinator.gateway import CoordinatorGateway
from app.coordinator.router import CoordinatorRouter
from app.domain.messages import (
    CoordinatorTask,
    SubagentResult,
    TutorRequest,
    TutorResponse,
)


class Coordinator(CoordinatorGateway):
    def __init__(
        self,
        teaching_agent: BaseSubagent,
        pdf_rag_agent: Optional[BaseSubagent] = None,
    ) -> None:
        self.agents: Dict[str, BaseSubagent] = {
            "teaching_agent": teaching_agent,
            "pdf_rag_agent": pdf_rag_agent or PdfRagAgent(),
            "web_research_agent": WebResearchAgent(),
            "github_agent": GithubAgent(),
        }
        self.agents = {
            name: agent
            for name, agent in self.agents.items()
            if agent is not None
        }

        self.router = CoordinatorRouter()
        self.context_store = CoordinatorContextStore()
        self._task_to_request: Dict[str, str] = {}

    def submit_finding(self, task_id: str, finding: str) -> None:
        """Store a finding submitted by a subagent."""
        request_id = self._task_to_request.get(task_id)

        if request_id is not None:
            self.context_store.add_finding(request_id, finding)

    def request_context(self, task_id: str, topic: str) -> List[str]:
        """Return approved findings for a subagent task."""
        request_id = self._task_to_request.get(task_id)

        if request_id is None:
            return []

        return self.context_store.search_findings(request_id, topic)

    def request_follow_up(
        self,
        task: CoordinatorTask,
        objective: str,
    ) -> SubagentResult:
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
        final_findings: List[str] = []

        for agent_name in selected_agents:
            if agent_name not in self.agents:
                continue

            approved_context = {}

            if agent_name == "pdf_rag_agent":
                approved_context = {
                    "active_document_id": request.active_document_id,
                }

            if agent_name == "teaching_agent":
                approved_context = {
                    "findings": self.context_store.get_findings(
                        parent_request_id
                    ),
                    "active_document_id": request.active_document_id,
                }


            task = CoordinatorTask(
                task_id=str(uuid4()),
                parent_request_id=parent_request_id,
                assigned_agent=agent_name,
                objective="Process the user question",
                user_question=request.question,
                learner_level=request.learner_level,
                approved_context=approved_context,
            )

            self._task_to_request[task.task_id] = parent_request_id
            findings_before = self.context_store.get_findings(parent_request_id)
            result = self.dispatch(task)
            results.append(result)

            for finding in result.findings:
                self.submit_finding(task.task_id, finding)

            if agent_name == "teaching_agent":
                findings_after = self.context_store.get_findings(
                    parent_request_id
                )
                final_findings.extend(
                    findings_after[len(findings_before):]
                )

        if not results or all(result.status == "failed" for result in results):
            return TutorResponse(
                answer="The Coordinator could not complete the request.",
                status="failed",
            )

        if not final_findings:
            return TutorResponse(
                answer="The Coordinator could not create a teaching answer.",
                status="failed",
            )

        return TutorResponse(
            answer="\n\n".join(final_findings),
            status="success",
        )
