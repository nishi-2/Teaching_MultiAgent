from typing import List

from app.retrieval.embeddings import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [
            [float(len(text)), 1.0]
            for text in texts
        ]


def test_embedding_provider_returns_one_vector_per_text() -> None:
    provider = FakeEmbeddingProvider()
    vectors = provider.embed_texts(["Python", "Docker"])

    assert len(vectors) == 2
    assert vectors[0] == [6.0, 1.0]
    assert vectors[1] == [6.0, 1.0]
