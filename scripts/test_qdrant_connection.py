from app.config.settings import settings
from app.retrieval.qdrant_store import QdrantStore


store = QdrantStore(settings=settings)
store.ensure_collection(vector_size=1536)

collection = store.client.get_collection(store.collection_name)

print(f"Collection: {store.collection_name}")
print(f"Collection status: {collection.status}")
