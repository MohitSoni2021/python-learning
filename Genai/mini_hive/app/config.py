"""Application configuration module."""

import os


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "mini_hive_memory")
QDRANT_TIMEOUT = float(os.getenv("QDRANT_TIMEOUT", "10"))

EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text:latest")