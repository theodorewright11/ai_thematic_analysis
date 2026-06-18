"""Load and normalize thematic-analysis data.

Two inputs feed every downstream step:

* the comment corpus (a markdown file in ``[Dn] body`` form), and
* one rating file per experimental condition (the human-rated export of a
  themeset).

This module turns both into typed records so metric and embedding code never
touches raw JSON shapes. Key normalization rules, all driven by how the data
actually varies across conditions:

* The quote array was renamed ``supporting`` -> ``quotes`` mid-project; both
  names are accepted.
* A node counts as a *theme* only if it carries at least one non-null rating.
  This drops the parent/container nodes in the human hierarchy (all-null
  ratings) while keeping the real, rated subthemes as the unit of analysis.
* A quote ``source`` of ``"N/A ..."`` (the low-effort condition) is treated as
  unattributed (``None``).
* The low-effort condition cites comments inside the definition text
  (``Representative comments: D2, D4, ...``) instead of via quote sources; those
  ids are parsed out into ``cited_sources``.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

#: The five rating dimensions, in display order. ``grounding`` and
#: ``aiPriorNovelty`` are legitimately null for the no-data condition.
RATING_DIMS: tuple[str, ...] = (
    "grounding",
    "researchQuestionFit",
    "interpretationLevel",
    "aiPriorNovelty",
    "analyticalNovelty",
)

_QUOTE_KEYS: tuple[str, ...] = ("quotes", "supporting")
_DX_RE = re.compile(r"D\d+")
_REPRESENTATIVE_RE = re.compile(r"Representative comments?:\s*([^.]*)", re.IGNORECASE)
_COMMENT_MARKER_RE = re.compile(r"\[(D\d+)\]")


@dataclass(frozen=True)
class Quote:
    """A supporting extract attached to a theme."""

    text: str
    source: str | None  # comment id (e.g. "D2"); None when unattributed
    role: str  # "core" | "supporting"


@dataclass(frozen=True)
class SimilarityLink:
    """A human-rated similarity from one theme to another in the same set."""

    other: str  # name of the other theme
    type: str  # "related" | "subsumes" | "subsumed-by"
    similarity: int  # 1-5 (5 = near-total overlap, 1 = minimal overlap)


@dataclass
class Theme:
    condition: str
    name: str
    definition: str | None
    reasoning: str | None
    parent: str | None
    ratings: dict[str, int | None]
    quotes: list[Quote]
    similarities: list[SimilarityLink]
    cited_sources: list[str]  # comment ids this theme points at

    @property
    def is_rated(self) -> bool:
        """True iff at least one rating dimension is filled. Container/parent
        nodes (all-null ratings) are not treated as themes."""
        return any(self.ratings.get(d) is not None for d in RATING_DIMS)

    def embed_text(self, include_definition: bool = True) -> str:
        """Text used to represent the theme for embedding. Falls back to the
        name alone when the definition is empty (some human subthemes)."""
        if include_definition and self.definition:
            return f"{self.name}\n\n{self.definition}"
        return self.name


@dataclass
class ThemeSet:
    condition: str
    path: str
    themes: list[Theme]

    @property
    def rated_themes(self) -> list[Theme]:
        return [t for t in self.themes if t.is_rated]


def load_comments(path: str | Path) -> dict[str, str]:
    """Parse a ``[Dn] body`` markdown corpus into ``{comment_id: text}``.

    Splitting on the ``[Dn]`` markers (rather than blank lines) keeps
    multi-paragraph comments intact.
    """
    text = Path(path).read_text(encoding="utf-8")
    parts = _COMMENT_MARKER_RE.split(text)
    comments: dict[str, str] = {}
    # parts = [preamble, id1, body1, id2, body2, ...]
    for i in range(1, len(parts), 2):
        cid = parts[i]
        body = parts[i + 1].strip()
        if body:
            comments[cid] = body
    return comments


def _parse_quote(raw: dict) -> Quote:
    source = raw.get("source")
    if not isinstance(source, str) or not source.strip() or "N/A" in source:
        source = None
    return Quote(text=raw.get("text", ""), source=source, role=raw.get("role") or "supporting")


def _extract_cited_sources(quotes: list[Quote], definition: str | None) -> list[str]:
    """Comment ids a theme references: quote sources first, then any
    ``Representative comments: D.., D..`` list embedded in the definition."""
    ids: list[str] = [q.source for q in quotes if q.source]
    if definition:
        match = _REPRESENTATIVE_RE.search(definition)
        if match:
            ids.extend(_DX_RE.findall(match.group(1)))
    seen: set[str] = set()
    out: list[str] = []
    for cid in ids:
        if cid not in seen:
            seen.add(cid)
            out.append(cid)
    return out


def load_theme_set(path: str | Path, condition: str) -> ThemeSet:
    """Parse one rating file into a :class:`ThemeSet`."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    themes: list[Theme] = []
    for node in data.get("themes", []):
        raw_quotes = next((node[k] for k in _QUOTE_KEYS if node.get(k)), [])
        quotes = [_parse_quote(q) for q in raw_quotes]
        raw_ratings = node.get("ratings") or {}
        ratings = {d: raw_ratings.get(d) for d in RATING_DIMS}
        similarities = [
            SimilarityLink(other=s["other"], type=s.get("type", ""), similarity=int(s["similarity"]))
            for s in (node.get("similarities") or [])
            if s.get("similarity") is not None and s.get("other")
        ]
        definition = node.get("definition") or None
        themes.append(
            Theme(
                condition=condition,
                name=node["name"],
                definition=definition,
                reasoning=node.get("reasoning") or None,
                parent=node.get("parent"),
                ratings=ratings,
                quotes=quotes,
                similarities=similarities,
                cited_sources=_extract_cited_sources(quotes, definition),
            )
        )
    return ThemeSet(condition=condition, path=str(path), themes=themes)


def load_all(rating_files: dict[str, str | Path]) -> dict[str, ThemeSet]:
    """Load every condition. ``rating_files`` maps condition name -> file path."""
    return {cond: load_theme_set(path, cond) for cond, path in rating_files.items()}


def rated_similarity_pairs(theme_set: ThemeSet) -> list[tuple[str, str, float, list[str]]]:
    """Unordered, deduped theme pairs that received a human similarity rating.

    Returns ``(name_a, name_b, mean_similarity, types)`` where the mean collapses
    both directions (A->B and B->A) when both were rated.
    """
    scores: dict[frozenset[str], list[int]] = defaultdict(list)
    types: dict[frozenset[str], list[str]] = defaultdict(list)
    for theme in theme_set.rated_themes:
        for link in theme.similarities:
            key = frozenset((theme.name, link.other))
            if len(key) != 2:  # guard against a self-referential link
                continue
            scores[key].append(link.similarity)
            types[key].append(link.type)
    pairs: list[tuple[str, str, float, list[str]]] = []
    for key, sims in scores.items():
        name_a, name_b = sorted(key)
        pairs.append((name_a, name_b, float(np.mean(sims)), types[key]))
    return pairs
