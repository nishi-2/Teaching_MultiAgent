from typing import Any, Dict, List, Optional
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.config.settings import Settings


class QdrantStore:
    """Manages the tutor document collection in Qdrant."""

    def __init__(
        self,
        settings: Settings,
        client: Optional[QdrantClient] = None,
    ) -> None:
        self.settings = settings
        self.client = client or QdrantClient(url=settings.qdrant_url)
        self.collection_name = settings.qdrant_collection

    def ensure_collection(self, vector_size: int = 1536) -> None:
        """Create the document collection if it does not already exist."""
        if self.client.collection_exists(self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert_vectors(
        self,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
    ) -> None:
        """Store vectors and their metadata in Qdrant."""
        if len(vectors) != len(payloads):
            raise ValueError("vectors and payloads must have the same length.")

        if not vectors:
            return

        self.ensure_collection(vector_size=len(vectors[0]))

        points = [
            PointStruct(
                id=str(uuid4()),
                vector=vector,
                payload=payload,
            )
            for vector, payload in zip(vectors, payloads)
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )


    def search_vectors(
        self,
        query_vector: List[float],
        limit: int = 5,
        document_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Search vectors, optionally restricted to one document."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero.")

        query_filter = None
        if document_id:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            )

        search_kwargs: Dict[str, Any] = {
            "collection_name": self.collection_name,
            "query": query_vector,
            "with_payload": True,
            "limit": limit,
        }

        if query_filter is not None:
            search_kwargs["query_filter"] = query_filter

        results = self.client.query_points(**search_kwargs).points

        return [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload or {},
            }
            for point in results
        ]
