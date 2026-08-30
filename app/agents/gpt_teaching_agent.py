from typing import Optional

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
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a patient technical teacher. "
                    "Explain concepts clearly, accurately, and step by step. "
                    "If you are uncertain, say so instead of inventing facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create a {task.learner_level}-level teaching explanation "
                    f"for:\n{task.user_question}"
                ),
            },
        ]

        answer, usage = self.llm.complete(messages=messages)

        coordinator.submit_finding(
            task_id=task.task_id,
            finding=answer,
        )

        return SubagentResult(
            task_id=task.task_id,
            agent_name=self.name,
            status="success",
            metadata={
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "learner_level": task.learner_level,
            },
        )
