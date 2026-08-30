from dataclasses import dataclass
from pathlib import Path
from typing import List

from pypdf import PdfReader


@dataclass(frozen=True)
class PDFPage:
    page_number: int
    text: str


def extract_pdf_pages(file_path: str) -> List[PDFPage]:
    """Extract text from a PDF while preserving one-based page numbers."""
    path = Path(file_path)
    reader = PdfReader(str(path))
    pages: List[PDFPage] = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(
            PDFPage(
                page_number=index,
                text=text.strip(),
            )
        )

    return pages
