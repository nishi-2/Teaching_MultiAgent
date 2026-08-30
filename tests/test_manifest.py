from datetime import datetime, timezone

from app.domain.document import DocumentRecord
from app.ingestion.manifest import IngestionManifest


def test_manifest_saves_and_loads_document(tmp_path) -> None:
    manifest_path = tmp_path / "documents.json"
    manifest = IngestionManifest(str(manifest_path))

    now = datetime.now(timezone.utc)
    document = DocumentRecord(
        document_id="document-1",
        file_name="sample.pdf",
        file_path="data/documents/sample.pdf",
        file_hash="a" * 64,
        status="indexed",
        page_count=2,
        chunk_count=4,
        created_at=now,
        updated_at=now,
    )

    manifest.save({document.document_id: document})
    loaded = manifest.load()

    assert loaded["document-1"].file_name == "sample.pdf"
    assert loaded["document-1"].status == "indexed"
    assert loaded["document-1"].chunk_count == 4
