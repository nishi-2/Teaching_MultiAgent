from dataclasses import dataclass
from typing import List

from app.retrieval.pdf_loader import PDFPage


@dataclass(frozen=True)
class TextChunk:
    page_number: int
    chunk_index: int
    text: str


def chunk_pages(pages: List[PDFPage], max_words: int = 200, overlap_words: int = 40,) -> List[TextChunk]:
    """Split PDF pages into overlapping chunks while preserving page numbers."""
    if max_words <= 0:
        raise ValueError("max_words must be greater than zero.")

    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("overlap_words must be between zero and max_words - 1.")

    chunks: List[TextChunk] = []

    for page in pages:
        words = page.text.split()
        start = 0
        chunk_index = 0

        while start < len(words):
            end = min(start + max_words, len(words))
            text = " ".join(words[start:end]).strip()

            if text:
                chunks.append(TextChunk(page_number=page.page_number, chunk_index=chunk_index, text=text,))

            if end == len(words):
                break

            start = end - overlap_words
            chunk_index += 1

    return chunks
