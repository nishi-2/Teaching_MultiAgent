# This uses the document metadata model to persist indexing state between runs

import json
from pathlib import Path
from typing import Dict

from app.domain.document import DocumentRecord


class IngestionManifest:
    """Persists document indexing metadata in a JSON file."""

    def __init__(self, manifest_path: str = "data/manifests/documents.json") -> None:
        self.path = Path(manifest_path)

    def load(self) -> Dict[str, DocumentRecord]:
        """Load document records from disk."""
        if not self.path.exists():
            return {}

        data = json.loads(self.path.read_text(encoding="utf-8"))
        return {
            document_id: DocumentRecord.model_validate(record)
            for document_id, record in data.items()
        }

    def save(self, records: Dict[str, DocumentRecord]) -> None:
        """Save document records to disk."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            document_id: record.model_dump(mode="json")
            for document_id, record in records.items()
        }
        self.path.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def list_documents(self) -> list[DocumentRecord]:
        """Return all tracked documents."""
        return list(self.load().values())

