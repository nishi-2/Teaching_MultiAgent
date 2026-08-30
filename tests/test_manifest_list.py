from datetime import datetime, timezone

from app.domain.document import DocumentRecord
from app.ingestion.manifest import IngestionManifest


def test_manifest_lists_documents(tmp_path) -> None:
    manifest = IngestionManifest(
        str(tmp_path / "documents.json")
    )
    now = datetime.now(timezone.utc)
    document = DocumentRecord(
        document_id="document-1",
        file_name="lesson.pdf",
        file_path="data/documents/lesson.pdf",
        file_hash="b" * 64,
        status="indexed",
        page_count=5,
        chunk_count=10,
        created_at=now,
        updated_at=now,
    )

    manifest.save({document.document_id: document})
    documents = manifest.list_documents()

    assert len(documents) == 1
    assert documents[0].file_name == "lesson.pdf"
    assert documents[0].page_count == 5
    assert documents[0].chunk_count == 10
