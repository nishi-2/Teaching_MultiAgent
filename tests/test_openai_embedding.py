from types import SimpleNamespace

from app.config.settings import Settings
from app.retrieval.openai_embeddings import OpenAIEmbeddingProvider


class FakeEmbeddings:
    def create(self, **kwargs):
        assert kwargs["model"] == "text-embedding-3-small"
        assert kwargs["input"] == ["Python", "Docker"]
        return SimpleNamespace(
            data=[
                SimpleNamespace(embedding=[0.1, 0.2]),
                SimpleNamespace(embedding=[0.3, 0.4]),
            ]
        )


class FakeOpenAIClient:
    def __init__(self):
        self.embeddings = FakeEmbeddings()


def test_openai_embedding_provider_returns_vectors() -> None:
    provider = OpenAIEmbeddingProvider(
        settings=Settings(
            openai_embedding_model="text-embedding-3-small"
        ),
        client=FakeOpenAIClient(),
    )

    vectors = provider.embed_texts(["Python", "Docker"])

    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
