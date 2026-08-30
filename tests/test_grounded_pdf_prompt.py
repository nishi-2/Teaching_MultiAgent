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


class RecordingLLM:
    def __init__(self):
        self.messages = []

    def complete(self, messages):
        self.messages = messages
        return "Grounded PDF teaching answer", UsageRecord()


class FakePDFAgent(BaseSubagent):
    name = "pdf_rag_agent"

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        coordinator.submit_finding(
            task_id=task.task_id,
            finding=(
                "PDF source: sample.pdf | page 1 | similarity 0.9500\n"
                "The document explains Model Context Protocol."
            ),
        )
        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
        )


def test_gpt_receives_approved_pdf_context() -> None:
    fake_llm = RecordingLLM()
    teaching_agent = GPTTeachingAgent(
        settings=Settings(openai_model="gpt-5-mini"),
        llm=fake_llm,
    )
    coordinator = Coordinator(
        teaching_agent=teaching_agent,
        pdf_rag_agent=FakePDFAgent(),
    )

    response = coordinator.handle_request(
        TutorRequest(
            question="Explain the main topic from my uploaded PDF document."
        )
    )

    prompt = fake_llm.messages[1]["content"]

    assert response.status == "success"
    assert "APPROVED PDF EVIDENCE" in prompt
    assert "PDF source: sample.pdf" in prompt
    assert "Model Context Protocol" in prompt
    assert "Do not say that the document is missing" in prompt
    assert "Grounded PDF teaching answer" in response.answer
    assert "PDF source: sample.pdf" not in response.answer
