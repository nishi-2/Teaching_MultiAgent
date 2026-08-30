from app.config.settings import Settings
from app.retrieval.qdrant_store import QdrantStore


class FakeQdrantClient:
    def __init__(self):
        self.exists = False
        self.created_collection = None

    def collection_exists(self, collection_name):
        return self.exists

    def create_collection(self, collection_name, vectors_config):
        self.created_collection = collection_name
        self.exists = True


def test_qdrant_store_creates_collection() -> None:
    fake_client = FakeQdrantClient()
    store = QdrantStore(
        settings=Settings(qdrant_collection="test_documents"),
        client=fake_client,
    )

    store.ensure_collection(vector_size=1536)

    assert fake_client.created_collection == "test_documents"
    assert fake_client.exists is True


def test_qdrant_store_does_not_recreate_collection() -> None:
    fake_client = FakeQdrantClient()
    fake_client.exists = True
    store = QdrantStore(settings=Settings(), client=fake_client)

    store.ensure_collection()

    assert fake_client.created_collection is None
