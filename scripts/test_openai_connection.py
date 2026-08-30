from app.config.settings import settings
from app.llm.client import OpenAIClientAdapter


adapter = OpenAIClientAdapter(settings=settings)
answer, usage = adapter.complete(
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: GPT connection successful.",
        }
    ]
)

print(answer)
print(f"Total tokens: {usage.total_tokens}")
