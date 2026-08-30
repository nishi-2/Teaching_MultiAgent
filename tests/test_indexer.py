from pathlib import Path
from typing import Dict, List

from app.ingestion.indexer import DocumentIndexer
from app.ingestion.manifest import IngestionManifest
from app.retrieval.embeddings import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [[float(index), 1.0] for index, _ in enumerate(texts)]


class FakeQdrantStore:
    def __init__(self):
        self.vectors: List[List[float]] = []
        self.payloads: List[Dict] = []

    def upsert_vectors(self, vectors, payloads) -> None:
        self.vectors = vectors
        self.payloads = payloads


def test_document_indexer_stores_vectors_and_metadata(
    tmp_path: Path,
) -> None:
    manifest = IngestionManifest(str(tmp_path / "documents.json"))
    store = FakeQdrantStore()
    indexer = DocumentIndexer(
        embedder=FakeEmbeddingProvider(),
        store=store,
        manifest=manifest,
    )

    record = indexer.index_file("data/documents/sample.pdf")

    assert record.status == "indexed"
    assert len(store.vectors) == record.chunk_count
    assert len(store.payloads) == record.chunk_count
    assert store.payloads[0]["file_name"] == "sample.pdf"
    assert "page_number" in store.payloads[0]
    assert "text" in store.payloads[0]
