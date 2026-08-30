from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


AgentName = Literal["teaching_agent", "pdf_rag_agent", "web_research_agent",
                    "github_agent", "citation_agent", "composer_agent",]

TaskStatus = Literal["success", "partial", "failed", "abstain"]
LearnerLevel = Literal["beginner", "intermediate", "advanced"]


class TutorRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    learner_level: LearnerLevel = "beginner"


class TutorResponse(BaseModel):
    answer: str
    status: Literal["success", "failed"] = "success"


class CoordinatorTask(BaseModel):
    task_id: str
    parent_request_id: str
    assigned_agent: AgentName
    objective: str
    user_question: str
    learner_level: LearnerLevel = "beginner"
    approved_context: dict[str, Any] = Field(default_factory=dict)
    max_steps: int = 5
    timeout_seconds: int = 30


class SubagentResult(BaseModel):
    task_id: str
    agent_name: AgentName
    status: TaskStatus
    findings: list[str] = Field(default_factory=list)
    requested_context: list[str] = Field(default_factory=list)
    follow_up_objective: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)
