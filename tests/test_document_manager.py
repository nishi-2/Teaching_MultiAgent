from pathlib import Path

import pytest

from app.ui.document_manager import save_uploaded_pdf


class FakeUploadedFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self.content = content

    def getbuffer(self) -> bytes:
        return self.content


def test_save_uploaded_pdf_uses_safe_filename(tmp_path: Path) -> None:
    uploaded_file = FakeUploadedFile(
        name="..\\private\\lesson.pdf",
        content=b"PDF test content",
    )

    saved_path = save_uploaded_pdf(
        uploaded_file,
        documents_dir=str(tmp_path),
    )

    assert Path(saved_path).name == "lesson.pdf"
    assert Path(saved_path).read_bytes() == b"PDF test content"


def test_save_uploaded_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    uploaded_file = FakeUploadedFile(
        name="lesson.txt",
        content=b"Not a PDF",
    )

    with pytest.raises(ValueError, match="Only PDF"):
        save_uploaded_pdf(
            uploaded_file,
            documents_dir=str(tmp_path),
        )
