from types import SimpleNamespace

import pytest

from app.config.settings import Settings
from app.llm.client import OpenAIClientAdapter


class EmptyCompletions:
    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=None),
                    finish_reason="length",
                )
            ]
        )


class EmptyOpenAIClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=EmptyCompletions())


def test_openai_adapter_rejects_empty_response() -> None:
    adapter = OpenAIClientAdapter(
        settings=Settings(openai_model="gpt-5-mini"),
        client=EmptyOpenAIClient(),
    )

    with pytest.raises(RuntimeError, match="no visible text"):
        adapter.complete(
            messages=[
                {"role": "user", "content": "Test empty response"}
            ]
        )
