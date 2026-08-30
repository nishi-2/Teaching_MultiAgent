from typing import Literal, Optional

from pydantic import BaseModel, Field


class PDFEvidence(BaseModel):
    """A verified excerpt retrieved from a local PDF."""

    source_type: Literal["pdf"] = "pdf"
    document_id: str
    file_name: str
    page_number: int = Field(ge=1)
    excerpt: str = Field(min_length=1)
    similarity_score: float = Field(ge=0.0, le=1.0)
    source_uri: Optional[str] = None

    def citation_label(self) -> str:
        """Return a readable citation label for this evidence."""
        return f"{self.file_name}, page {self.page_number}"
