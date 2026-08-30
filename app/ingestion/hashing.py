# This hash will let us detect whether a PDF is new or has changed before re-indexing it. 

import hashlib
from pathlib import Path


def calculate_file_hash(file_path: str) -> str:
    """Calculate a stable SHA-256 hash for a document."""
    path = Path(file_path)
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()
