from app.retrieval.chunking import chunk_pages
from app.retrieval.pdf_loader import PDFPage


def test_chunk_pages_preserves_page_numbers() -> None:
    pages = [
        PDFPage(
            page_number=3,
            text="one two three four five six seven eight nine ten",
        )
    ]

    chunks = chunk_pages(
        pages,
        max_words=4,
        overlap_words=1,
    )

    assert len(chunks) == 3
    assert all(chunk.page_number == 3 for chunk in chunks)
    assert chunks[0].text == "one two three four"
    assert chunks[1].text == "four five six seven"
    assert chunks[2].text == "seven eight nine ten"


def test_chunk_pages_rejects_invalid_overlap() -> None:
    pages = [PDFPage(page_number=1, text="sample text")]

    try:
        chunk_pages(pages, max_words=10, overlap_words=10)
    except ValueError as error:
        assert "overlap_words" in str(error)
    else:
        raise AssertionError("Expected ValueError for invalid overlap")
