from datetime import datetime, timezone
from pathlib import Path

from app.domain.document import DocumentRecord
from app.ingestion.hashing import calculate_file_hash
from app.ingestion.manifest import IngestionManifest
from app.retrieval.chunking import chunk_pages
from app.retrieval.pdf_loader import extract_pdf_pages


class PDFIngestionPipeline:
    """Extract and record a PDF before vector indexing is added."""

    def __init__(self, manifest: IngestionManifest | None = None,) -> None:
        self.manifest = manifest or IngestionManifest()

    def ingest_file(self, file_path: str) -> DocumentRecord:
        """Extract one PDF and persist its document metadata."""
        path = Path(file_path)
        file_hash = calculate_file_hash(str(path))
        document_id = file_hash[:16]
        now = datetime.now(timezone.utc)

        try:
            pages = extract_pdf_pages(str(path))
            chunks = chunk_pages(pages)

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
