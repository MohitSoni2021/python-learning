"""Embedding model configuration and utilities."""

from langchain_ollama import OllamaEmbeddings

from app.config import EMBED_MODEL


def get_embedder(model: str | None = None) -> OllamaEmbeddings:
	"""Create an Ollama embedding client.

	Args:
		model: Optional model override. Uses EMBED_MODEL if omitted.
	"""
	return OllamaEmbeddings(model=model or EMBED_MODEL)
