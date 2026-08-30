from pathlib import Path
from typing import Any


def save_uploaded_pdf(
    uploaded_file: Any,
    documents_dir: str = "data/documents",
) -> str:
    """Save an uploaded PDF safely inside the documents directory."""
    original_name = Path(uploaded_file.name).name

    if not original_name.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are supported.")

    target_dir = Path(documents_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / original_name
    target_path.write_bytes(uploaded_file.getbuffer())

    return str(target_path)
