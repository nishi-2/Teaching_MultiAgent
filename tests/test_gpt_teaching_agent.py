from app.agents.gpt_teaching_agent import GPTTeachingAgent
from app.config.settings import Settings
from app.coordinator.coordinator import Coordinator
from app.domain.messages import TutorRequest
from app.llm.usage import UsageRecord


class FakeLLM:
    def complete(self, messages):
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        return (
            "Mock GPT teaching answer",
            UsageRecord(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
            ),
        )


def test_gpt_teaching_agent_uses_llm_and_coordinator() -> None:
    teaching_agent = GPTTeachingAgent(
        settings=Settings(openai_model="gpt-5-mini"),
        llm=FakeLLM(),
    )
    coordinator = Coordinator(teaching_agent=teaching_agent)

    response = coordinator.handle_request(
        TutorRequest(question="Explain Python variables.")
    )

    assert response.status == "success"
    assert "Mock GPT teaching answer" in response.answer
