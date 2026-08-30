from dataclasses import dataclass
from typing import Any, Optional

@dataclass(frozen=True)
class UsageRecord:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


def extract_usage(response: Any) -> UsageRecord:
    """Extract token usage safely from an OpenAI response."""
    usage: Optional[Any] = getattr(response, "usage", None)

    if usage is None:
        return UsageRecord()

    prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
    total_tokens = int(getattr(usage, "total_tokens", 0) or 0)

    return UsageRecord(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )