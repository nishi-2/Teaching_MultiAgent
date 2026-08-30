# To keep the RAG pipeline independent from a specific embedding provider

from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """Interface for converting text into vectors."""

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Create one vector for each input text."""
        raise NotImplementedError
