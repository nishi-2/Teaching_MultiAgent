from app.agents.gpt_teaching_agent import GPTTeachingAgent
from app.config.settings import Settings
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest
from app.llm.usage import UsageRecord


class RecordingLLM:
    def __init__(self):
        self.messages = []

    def complete(self, messages):
        self.messages = messages
        return (
            "Recorded teaching response",
            UsageRecord(),
        )


def test_learner_level_is_sent_to_gpt_prompt() -> None:
    fake_llm = RecordingLLM()
    teaching_agent = GPTTeachingAgent(
        settings=Settings(openai_model="gpt-5-mini"),
        llm=fake_llm,
    )
    coordinator = Coordinator(teaching_agent=teaching_agent)

    coordinator.handle_request(
        TutorRequest(
            question="Explain Docker containers.",
            learner_level="advanced",
        )
    )

    user_prompt = fake_llm.messages[1]["content"]
    assert "advanced-level" in user_prompt
    assert "Docker containers" in user_prompt
