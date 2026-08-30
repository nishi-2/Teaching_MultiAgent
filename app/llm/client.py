from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from app.config.settings import Settings
from app.llm.models import get_gpt_model_config
from app.llm.usage import UsageRecord, extract_usage


class OpenAIClientAdapter:
    """Centralized OpenAI GPT client used by application agents."""

    def __init__(
        self,
        settings: Settings,
        client: Optional[OpenAI] = None,
    ) -> None:
        self.settings = settings
        self.model_config = get_gpt_model_config(settings)
        self.client = client or OpenAI(api_key=settings.openai_api_key)

    def complete(
        self,
        messages: List[Dict[str, str]],
    ) -> Tuple[str, UsageRecord]:
        """Request text from GPT and return text together with usage."""
        response = self.client.chat.completions.create(
            model=self.model_config.name,
            messages=messages,
            max_completion_tokens=4000,
        )

        message = response.choices[0].message
        content: Any = message.content

        if not content:
            finish_reason = response.choices[0].finish_reason
            raise RuntimeError(
                f"OpenAI returned no visible text. Finish reason: {finish_reason}"
            )

        return content, extract_usage(response)
