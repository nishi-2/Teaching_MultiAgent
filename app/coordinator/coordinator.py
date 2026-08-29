from uuid import uuid4
from app.agents.base import BaseSubagent
from app.domain.messages import CoordinatorTask, SubagentResult, TutorRequest, TutorResponse

class Coordinator:
    def __init__(self, teaching_agent: BaseSubagent) -> None:
        self.teaching_agent = teaching_agent

    def handle_request(self, request: TutorRequest) -> TutorResponse:
        parent_request_id = str(uuid4)

        task = CoordinatorTask(
            task_id= str(uuid4()),
            parent_request_id= parent_request_id,
            assigned_agent="teaching_agent",
            objective="Create a teaching plan",
            user_question=request.question
        )
        result: SubagentResult = self.teaching_agent.run(task)

        if result.status == "failed":
            return TutorResponse(
                answer="The Coordinator could not complete the request.",
                status="failed",
            )

        answer = '\n'.join(result.findings)
        return TutorResponse(answer=answer, status="success")