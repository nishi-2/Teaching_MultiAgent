from app.config.settings import settings
from app.ingestion.indexer import DocumentIndexer
from app.ingestion.manifest import IngestionManifest
from app.retrieval.openai_embeddings import OpenAIEmbeddingProvider
from app.retrieval.qdrant_store import QdrantStore


embedder = OpenAIEmbeddingProvider(settings=settings)
store = QdrantStore(settings=settings)
manifest = IngestionManifest()
indexer = DocumentIndexer(
    embedder=embedder,
    store=store,
    manifest=manifest,
)

record = indexer.index_file("data/documents/sample.pdf")

print(f"Document: {record.file_name}")
print(f"Status: {record.status}")
print(f"Pages: {record.page_count}")
print(f"Chunks: {record.chunk_count}")
