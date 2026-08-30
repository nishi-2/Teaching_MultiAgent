from app.config.settings import Settings
from app.retrieval.qdrant_store import QdrantStore


class FakeQdrantClient:
    def __init__(self):
        self.points = []

    def collection_exists(self, collection_name):
        return True

    def upsert(self, collection_name, points, wait):
        self.points.extend(points)


def test_qdrant_store_upserts_vectors_and_payloads() -> None:
    fake_client = FakeQdrantClient()
    store = QdrantStore(
        settings=Settings(),
        client=fake_client,
    )

    store.upsert_vectors(
        vectors=[[0.1, 0.2], [0.3, 0.4]],
        payloads=[
            {"page_number": 1, "text": "Python"},
            {"page_number": 2, "text": "Docker"},
        ],
    )

    assert len(fake_client.points) == 2
    assert fake_client.points[0].payload["page_number"] == 1
    assert fake_client.points[1].payload["text"] == "Docker"


def test_qdrant_store_rejects_mismatched_lengths() -> None:
    fake_client = FakeQdrantClient()
    store = QdrantStore(settings=Settings(), client=fake_client)

    try:
        store.upsert_vectors(
            vectors=[[0.1, 0.2]],
            payloads=[],
        )
    except ValueError as error:
        assert "same length" in str(error)
    else:
        raise AssertionError("Expected ValueError for mismatched lengths")
