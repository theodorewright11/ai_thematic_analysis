"""OpenAI embeddings with a persistent on-disk cache, plus cosine helpers.

Every text is keyed by ``sha256(model, text)`` so identical text is never
re-embedded across runs (the model name is part of the key, so switching models
does not collide). The API key is read from the environment or a ``.env`` file
at call time, so importing this module and computing ratings never requires a
key — only an actual embedding call does.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv

DEFAULT_MODEL = "text-embedding-3-large"
_BATCH = 256  # well under the OpenAI per-request input limit


def _key(model: str, text: str) -> str:
    return hashlib.sha256(f"{model}\x00{text}".encode("utf-8")).hexdigest()


class Embedder:
    """Cached embedding client. Call :meth:`embed` with a list of texts; it
    returns ``{text: vector}`` and only hits the API for cache misses."""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        cache_path: str | Path = "analysis/cache/embeddings.json",
    ) -> None:
        self.model = model
        self.cache_path = Path(cache_path)
        self._cache: dict[str, list[float]] = {}
        if self.cache_path.exists():
            self._cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
        self._client = None  # created lazily, only when an API call is needed

    def _ensure_client(self):
        if self._client is None:
            load_dotenv()
            if not os.environ.get("OPENAI_API_KEY"):
                raise RuntimeError(
                    "OPENAI_API_KEY not found. Add it to a .env file at the project root."
                )
            from openai import OpenAI

            self._client = OpenAI()
        return self._client

    def embed(self, texts: list[str]) -> dict[str, np.ndarray]:
        """Return ``{text: vector}`` for every non-empty text, using the cache
        and batching API calls for any misses."""
        unique = list(dict.fromkeys(t for t in texts if t))
        missing = [t for t in unique if _key(self.model, t) not in self._cache]
        for start in range(0, len(missing), _BATCH):
            batch = missing[start : start + _BATCH]
            response = self._ensure_client().embeddings.create(model=self.model, input=batch)
            for text, item in zip(batch, response.data):
                self._cache[_key(self.model, text)] = item.embedding
        if missing:
            self._save()
        return {t: np.asarray(self._cache[_key(self.model, t)], dtype=np.float64) for t in unique}

    def cost_estimate(self, texts: list[str]) -> dict[str, int]:
        """How many unique texts would hit the API, without calling it."""
        unique = list(dict.fromkeys(t for t in texts if t))
        misses = sum(1 for t in unique if _key(self.model, t) not in self._cache)
        return {"unique": len(unique), "cached": len(unique) - misses, "to_embed": misses}

    def _save(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.write_text(json.dumps(self._cache), encoding="utf-8")


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity of two vectors (0.0 if either is a zero vector)."""
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / norm) if norm else 0.0


def mean_cosine(vec: np.ndarray, others: list[np.ndarray]) -> float:
    """Mean cosine of ``vec`` against a list of vectors."""
    return float(np.mean([cosine(vec, o) for o in others])) if others else float("nan")
