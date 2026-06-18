"""Per-condition aggregates of the human ratings (no embeddings involved).

Means are taken over non-null values per dimension, so the no-data condition
(grounding and aiPriorNovelty are N/A) and any partially-rated human themes are
handled without dragging the average toward zero.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from load import RATING_DIMS, ThemeSet, rated_similarity_pairs


def _mean(values: list[float | int | None]) -> float | None:
    present = [v for v in values if v is not None]
    return float(np.mean(present)) if present else None


def rating_table(sets: dict[str, ThemeSet]) -> pd.DataFrame:
    """One row per condition: theme count, mean of each rating dimension, mean
    rated theme-similarity, and mean quotes per theme."""
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        themes = theme_set.rated_themes
        row: dict[str, object] = {"condition": condition, "n_themes": len(themes)}
        for dim in RATING_DIMS:
            row[dim] = _mean([t.ratings.get(dim) for t in themes])
        pairs = rated_similarity_pairs(theme_set)
        row["n_similarity_pairs"] = len(pairs)
        row["mean_similarity"] = _mean([p[2] for p in pairs])
        row["mean_quotes_per_theme"] = _mean([float(len(t.quotes)) for t in themes])
        rows.append(row)
    return pd.DataFrame(rows).set_index("condition")


def theme_rating_table(sets: dict[str, ThemeSet]) -> pd.DataFrame:
    """One row per rated theme with its ratings — the detailed-report backing."""
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        for theme in theme_set.rated_themes:
            row: dict[str, object] = {
                "condition": condition,
                "theme": theme.name,
                "n_quotes": len(theme.quotes),
                "n_cited_comments": len(theme.cited_sources),
            }
            row.update({dim: theme.ratings.get(dim) for dim in RATING_DIMS})
            rows.append(row)
    return pd.DataFrame(rows)
