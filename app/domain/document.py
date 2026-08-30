from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class DocumentRecord(BaseModel):
    """Metadata for a PDF known to the tutor system."""
    document_id: str
    file_name: str
    file_path: str
    file_hash: str
    status: Literal["discovered", "indexed", "failed"] = "discovered"
    page_count: Optional[int] = None
    chunk_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
