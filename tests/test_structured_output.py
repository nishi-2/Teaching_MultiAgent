import json
from types import SimpleNamespace

from app.config.settings import Settings
from app.llm.client import OpenAIClientAdapter
from app.llm.structured_output import StructuredOutputClient


class FakeCompletions:
    def create(self, **kwargs):
        assert kwargs["response_format"]["type"] == "json_schema"
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {
                                "topic": "Python",
                                "difficulty": "beginner",
                            }
                        )
                    )
                )
            ]
        )


class FakeOpenAIClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_structured_output_returns_json_object() -> None:
    adapter = OpenAIClientAdapter(
        settings=Settings(openai_model="gpt-5-mini"),
        client=FakeOpenAIClient(),
    )
    structured_client = StructuredOutputClient(adapter)

    result = structured_client.complete_json(
        messages=[
            {"role": "user", "content": "Create a learning topic."}
        ],
        schema_name="learning_topic",
        schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "difficulty": {"type": "string"},
            },
            "required": ["topic", "difficulty"],
            "additionalProperties": False,
        },
    )

    assert result["topic"] == "Python"
    assert result["difficulty"] == "beginner"
