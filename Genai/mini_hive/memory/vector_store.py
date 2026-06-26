"""Vector store integration (Qdrant)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.config import (
	QDRANT_API_KEY,
	QDRANT_COLLECTION,
	QDRANT_TIMEOUT,
	QDRANT_URL,
)
from models.embeddings import get_embedder


class QdrantMemoryStore:
	"""Simple semantic memory store backed by Qdrant."""

	def __init__(
		self,
		collection_name: str | None = None,
		url: str | None = None,
		api_key: str | None = None,
		timeout: float | None = None,
	) -> None:
		self.collection_name = collection_name or QDRANT_COLLECTION
		self.embedder = get_embedder()
		self.client = QdrantClient(
			url=url or QDRANT_URL,
			api_key=api_key or QDRANT_API_KEY,
			timeout=timeout or QDRANT_TIMEOUT,
		)
		self._is_collection_ready = False

	def health_check(self) -> bool:
		"""Return True when Qdrant responds to cluster info."""
		try:
			self.client.get_collections()
			return True
		except Exception:
			return False

	def ensure_collection(self) -> None:
		"""Create collection on first use if it does not exist."""
		if self._is_collection_ready:
			return

		if not self.client.collection_exists(collection_name=self.collection_name):
			probe_vector = self.embedder.embed_query("dimension_probe")
			vector_size = len(probe_vector)

			self.client.create_collection(
				collection_name=self.collection_name,
				vectors_config=qmodels.VectorParams(
					size=vector_size,
					distance=qmodels.Distance.COSINE,
				),
			)

		self._is_collection_ready = True

	def upsert_text(
		self,
		text: str,
		metadata: dict[str, Any] | None = None,
		point_id: str | None = None,
	) -> str:
		"""Insert or update a text memory and return the point id."""
		if not text or not text.strip():
			raise ValueError("text must be a non-empty string")

		self.ensure_collection()

		memory_id = point_id or str(uuid.uuid4())
		vector = self.embedder.embed_query(text)
		payload = {
			"text": text,
			"created_at": datetime.now(timezone.utc).isoformat(),
			**(metadata or {}),
		}

		self.client.upsert(
			collection_name=self.collection_name,
			points=[
				qmodels.PointStruct(
					id=memory_id,
					vector=vector,
					payload=payload,
				)
			],
		)

		return memory_id

	def search(
		self,
		query: str,
		limit: int = 3,
		score_threshold: float | None = None,
	) -> list[dict[str, Any]]:
		"""Semantic search over stored memory payloads."""
		if not query or not query.strip():
			return []

		self.ensure_collection()
		query_vector = self.embedder.embed_query(query)

		results = self.client.search(
			collection_name=self.collection_name,
			query_vector=query_vector,
			limit=limit,
			score_threshold=score_threshold,
		)

		return [
			{
				"id": str(item.id),
				"score": item.score,
				"payload": item.payload or {},
			}
			for item in results
		]


def create_qdrant_store() -> QdrantMemoryStore:
	"""Factory for use by services and graph nodes."""
	return QdrantMemoryStore()
