from app.agents.base import BaseSubagent
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult


class PdfRagAgent(BaseSubagent):
    name = "pdf_rag_agent"

    def run(self, task: CoordinatorTask, coordinator: CoordinatorGateway,) -> SubagentResult:
        coordinator.submit_finding(task.task_id, "PDF RAG Agent received the document-related question.",)
        return SubagentResult(task_id=task.task_id, agent_name=self.name, status="success",)


class WebResearchAgent(BaseSubagent):
    name = "web_research_agent"

    def run(self, task: CoordinatorTask, coordinator: CoordinatorGateway,) -> SubagentResult:
        coordinator.submit_finding(task.task_id, "Web Research Agent received the current-information question.",)
        return SubagentResult(task_id=task.task_id, agent_name=self.name, status="success",)


class GithubAgent(BaseSubagent):
    name = "github_agent"

    def run(self, task: CoordinatorTask, coordinator: CoordinatorGateway,) -> SubagentResult:
        coordinator.submit_finding(task.task_id, "GitHub Agent received the repository-related question.",)
        return SubagentResult(task_id=task.task_id, agent_name=self.name, status="success",)
