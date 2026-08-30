from datetime import datetime, timezone
from pathlib import Path

from app.domain.document import DocumentRecord
from app.ingestion.hashing import calculate_file_hash
from app.ingestion.manifest import IngestionManifest
from app.retrieval.chunking import chunk_pages
from app.retrieval.embeddings import EmbeddingProvider
from app.retrieval.pdf_loader import extract_pdf_pages
from app.retrieval.qdrant_store import QdrantStore


class DocumentIndexer:
    """Indexes PDF chunks as vectors with page-aware metadata."""

    def __init__(
        self,
        embedder: EmbeddingProvider,
        store: QdrantStore,
        manifest: IngestionManifest | None = None,
    ) -> None:
        self.embedder = embedder
        self.store = store
        self.manifest = manifest or IngestionManifest()

    def index_file(self, file_path: str) -> DocumentRecord:
        """Extract, embed, and store one PDF."""
        path = Path(file_path)
        file_hash = calculate_file_hash(str(path))
        document_id = file_hash[:16]
        now = datetime.now(timezone.utc)

        try:
            pages = extract_pdf_pages(str(path))
            chunks = chunk_pages(pages)
            vectors = self.embedder.embed_texts(
                [chunk.text for chunk in chunks]
            )
            payloads = [
                {
                    "document_id": document_id,
                    "file_name": path.name,
                    "file_hash": file_hash,
                    "page_number": chunk.page_number,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
                for chunk in chunks
            ]

            self.store.upsert_vectors(vectors, payloads)

            record = DocumentRecord(
                document_id=document_id,
                file_name=path.name,
                file_path=str(path),
                file_hash=file_hash,
                status="indexed",
                page_count=len(pages),
                chunk_count=len(chunks),
                created_at=now,
                updated_at=now,
            )
        except Exception as error:
            record = DocumentRecord(
                document_id=document_id,
                file_name=path.name,
                file_path=str(path),
                file_hash=file_hash,
                status="failed",
                error_message=str(error),
                created_at=now,
                updated_at=now,
            )

        records = self.manifest.load()
        records[document_id] = record
        self.manifest.save(records)
        return record
