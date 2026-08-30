from typing import List

from app.agents.base import BaseSubagent
from app.agents.gpt_teaching_agent import GPTTeachingAgent
from app.config.settings import Settings
from app.coordinator.coordinator import Coordinator
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import (
    CoordinatorTask,
    SubagentResult,
    TutorRequest,
)
from app.llm.usage import UsageRecord


class RecordingPDFAgent(BaseSubagent):
    name = "pdf_rag_agent"

    def __init__(self):
        self.received_context = {}

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        self.received_context = task.approved_context
        coordinator.submit_finding(
            task_id=task.task_id,
            finding=(
                "PDF source: new.pdf | page 1 | similarity 0.9500\n"
                "Evidence from the newly selected document."
            ),
        )
        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
        )


class RecordingLLM:
    def __init__(self):
        self.messages = []

    def complete(self, messages):
        self.messages = messages
        return "Final answer based on the selected PDF.", UsageRecord()


def test_active_document_flows_to_pdf_and_gpt() -> None:
    fake_pdf_agent = RecordingPDFAgent()
    fake_llm = RecordingLLM()
    teaching_agent = GPTTeachingAgent(
        settings=Settings(openai_model="gpt-5-mini"),
        llm=fake_llm,
    )
    coordinator = Coordinator(
        teaching_agent=teaching_agent,
        pdf_rag_agent=fake_pdf_agent,
    )

    response = coordinator.handle_request(
        TutorRequest(
            question="Explain my uploaded PDF document.",
            active_document_id="new-document-id",
        )
    )

    prompt = fake_llm.messages[1]["content"]

    assert response.status == "success"
    assert fake_pdf_agent.received_context["active_document_id"] == (
        "new-document-id"
    )
    assert "new.pdf" in prompt
    assert "Evidence from the newly selected document." in prompt
    assert "Final answer based on the selected PDF." in response.answer
    assert "MCP" not in response.answer
