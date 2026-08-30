from pathlib import Path

from app.retrieval.pdf_loader import extract_pdf_pages


def test_extract_pdf_pages_preserves_page_numbers() -> None:
    pdf_path = Path("data/documents/sample.pdf")

    pages = extract_pdf_pages(str(pdf_path))

    assert len(pages) > 0
    assert pages[0].page_number == 1
    assert isinstance(pages[0].text, str)
