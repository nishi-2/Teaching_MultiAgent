from typing import Any, Optional

from app.agents.base import BaseSubagent
from app.config.settings import Settings
from app.coordinator.gateway import CoordinatorGateway
from app.domain.messages import CoordinatorTask, SubagentResult
from app.llm.client import OpenAIClientAdapter


class GPTTeachingAgent(BaseSubagent):
    name = "teaching_agent"

    def __init__(
        self,
        settings: Settings,
        llm: Optional[OpenAIClientAdapter] = None,
    ) -> None:
        self.llm = llm or OpenAIClientAdapter(settings=settings)

    def run(
        self,
        task: CoordinatorTask,
        coordinator: CoordinatorGateway,
    ) -> SubagentResult:
        findings = task.approved_context.get("findings", [])
        context_text = "\n\n".join(str(finding) for finding in findings)

        if context_text:
            evidence_instruction = (
                "The Coordinator supplied the following retrieved PDF evidence. "
                "Use it as the primary source for your answer. Preserve the PDF "
                "source filename and page references when making factual claims. "
                "Do not say that the document is missing. Do not ask the user "
                "to upload a document. If the evidence is insufficient, clearly "
                "state what cannot be determined from the supplied evidence.\n\n"
                "--- APPROVED PDF EVIDENCE ---\n"
                f"{context_text}\n"
                "--- END APPROVED PDF EVIDENCE ---"
            )
        else:
            evidence_instruction = (
                "No retrieved document evidence was supplied. Answer using only "
                "general knowledge and clearly state when a claim needs a source."
            )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a patient technical teacher. Explain concepts clearly, "
                    "accurately, and step by step. Never invent sources or facts. "
                    "Use the Coordinator-approved evidence when it is present."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create a {task.learner_level}-level teaching explanation for:\n"
                    f"{task.user_question}\n\n"
                    f"{evidence_instruction}\n\n"
                    "Return only the teaching explanation, not internal workflow "
                    "notes or a request for the user to upload the document."
                ),
            },
        ]

        answer, usage = self.llm.complete(messages=messages)

        coordinator.submit_finding(
            task_id=task.task_id,
            finding=answer,
        )

        metadata: dict[str, Any] = {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "learner_level": task.learner_level,
            "evidence_count": len(findings),
        }

        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            metadata=metadata,
        )
