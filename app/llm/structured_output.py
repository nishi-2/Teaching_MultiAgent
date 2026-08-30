import json
from typing import Any, Dict, List
from app.llm.client import OpenAIClientAdapter


class StructuredOutputClient:
    """ Requests strict JSON responses from the configured GPT Model """
    def __init__(self, adapter: OpenAIClientAdapter) -> None:
        self.adapter = adapter

    def complete_json(self, messages: List[Dict[str, str]], schema_name: str, schema: Dict[str, Any]) -> Dict[str, Any] :
        """Return a GPT response parsed as JSON using the supplied schema."""
        response = self.adapter.client.chat.completions.create(
            model=self.adapter.model_config.name,
            messages=messages,
            max_completion_tokens=1000,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                },
            },
        )
        content = response.choices[0].message.content

        if not content:
            raise RuntimeError("GPT returned an empty structured response.")

        parsed = json.loads(content)

        if not isinstance(parsed, dict):
            raise RuntimeError("GPT structured response must be a JSON object.")

        return parsed