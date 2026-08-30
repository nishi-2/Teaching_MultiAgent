import pytest

from app.domain.evidence import PDFEvidence


def test_pdf_evidence_creates_citation_label() -> None:
    evidence = PDFEvidence(
        document_id="document-1",
        file_name="sample.pdf",
        page_number=3,
        excerpt="The document explains Model Context Protocol.",
        similarity_score=0.95,
    )

    assert evidence.citation_label() == "sample.pdf, page 3"
    assert evidence.source_type == "pdf"


def test_pdf_evidence_rejects_invalid_page() -> None:
    with pytest.raises(ValueError):
        PDFEvidence(
            document_id="document-1",
            file_name="sample.pdf",
            page_number=0,
            excerpt="Invalid page",
            similarity_score=0.95,
        )


def test_pdf_evidence_rejects_invalid_similarity() -> None:
    with pytest.raises(ValueError):
        PDFEvidence(
            document_id="document-1",
            file_name="sample.pdf",
            page_number=1,
            excerpt="Invalid similarity",
            similarity_score=1.5,
        )
