from typing import Literal
from pydantic import BaseModel, Field

class TutorRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    learner_level: Literal["beginner", "intermediate", "advanced"] = "beginner"


class TutorResponse(BaseModel):
    answer: str
    status: Literal["success", "failed"] = "success"


class CoordinatorTask(BaseModel):
    task_id: str
    objective: str
    user_question: str


class SubagentResult(BaseModel):
    task_id: str
    agent_name: str
    status: Literal["success", "failed"]
    findings: list[str] = Field(default_factory=list)