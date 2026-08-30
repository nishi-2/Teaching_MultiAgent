from types import SimpleNamespace

from app.config.settings import Settings
from app.llm.client import OpenAIClientAdapter


class FakeCompletions:
    def create(self, **kwargs):
        assert kwargs["model"] == "gpt-5-mini"
        assert kwargs["max_completion_tokens"] == 4000
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Mock GPT response")
                )
            ],
            usage=SimpleNamespace(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30,
            ),
        )


class FakeOpenAIClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_openai_adapter_returns_text_and_usage() -> None:
    settings = Settings(openai_model="gpt-5-mini")
    adapter = OpenAIClientAdapter(
        settings=settings,
        client=FakeOpenAIClient(),
    )

    result, usage = adapter.complete(
        messages=[
            {"role": "user", "content": "What is Python?"}
        ]
    )

    assert result == "Mock GPT response"
    assert usage.prompt_tokens == 10
    assert usage.completion_tokens == 20
    assert usage.total_tokens == 30
