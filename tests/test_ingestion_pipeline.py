from pathlib import Path

from app.ingestion.manifest import IngestionManifest
from app.ingestion.pipeline import PDFIngestionPipeline


def test_ingestion_pipeline_records_pdf(tmp_path: Path) -> None:
    manifest = IngestionManifest(
        str(tmp_path / "documents.json")
    )
    pipeline = PDFIngestionPipeline(manifest=manifest)

    record = pipeline.ingest_file("data/documents/sample.pdf")

    assert record.status == "indexed"
    assert record.file_name == "sample.pdf"
    assert record.page_count is not None
    assert record.page_count > 0
    assert record.document_id in manifest.load()
