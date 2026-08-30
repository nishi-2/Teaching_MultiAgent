from typing import List, Optional

from openai import OpenAI

from app.config.settings import Settings
from app.retrieval.embeddings import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """Creates document vectors using the configured OpenAI embedding model."""

    def __init__(self, settings: Settings, client: Optional[OpenAI] = None,) -> None:
        self.settings = settings
        self.client = client or OpenAI(api_key=settings.openai_api_key)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Create one embedding vector for each text."""
        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.settings.openai_embedding_model,
            input=texts,
        )

        return [item.embedding for item in response.data]
