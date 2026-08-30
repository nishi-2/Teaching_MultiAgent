from types import SimpleNamespace

from app.config.settings import Settings
from app.retrieval.qdrant_store import QdrantStore


class FakeQdrantClient:
    def query_points(
        self,
        collection_name,
        query,
        with_payload,
        limit,
        query_filter=None,
    ):
        assert collection_name == "ai_tutor_documents"
        assert query == [0.1, 0.2]
        assert with_payload is True
        assert limit == 2

        return SimpleNamespace(
            points=[
                SimpleNamespace(
                    id="point-1",
                    score=0.95,
                    payload={"page_number": 1, "text": "Python"},
                )
            ]
        )


def test_qdrant_store_searches_vectors() -> None:
    store = QdrantStore(
        settings=Settings(),
        client=FakeQdrantClient(),
    )

    results = store.search_vectors(
        query_vector=[0.1, 0.2],
        limit=2,
    )

    assert len(results) == 1
    assert results[0]["id"] == "point-1"
    assert results[0]["score"] == 0.95
    assert results[0]["payload"]["text"] == "Python"
