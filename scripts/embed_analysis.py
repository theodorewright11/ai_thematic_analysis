"""Embedding-based analyses over themes, quotes, comments, and the RQ.

All cosine similarities use ``text-embedding-3-large`` vectors (via
:mod:`embed`). A theme is represented by its *name + definition* text unless
noted. Every function returns a tidy :class:`pandas.DataFrame` so the report
layer only formats — it never computes.

The five analyses, mapping to the research questions:

1. ``theme_rq_cosine``     - how close each theme sits to the research question.
2. ``quote_level_table``   - per-quote distances; backs the core-vs-supporting
   and interpretation-level contrasts, and the quote-to-data (provenance vs
   representativeness) view.
3. ``theme_cited_cosine``  - does a theme embed closer to the comments it cites
   than to the rest of the corpus (a grounding proxy, the only quote-free signal
   available for the low-effort condition, whose definitions cite ``Dn`` ids).
4. ``theme_pairs`` + ``similarity_validation`` - do embedding cosines reproduce
   the human 1-5 theme-similarity ratings, and is the implicit "unrated =
   independent" assumption borne out by low cosines?
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from embed import Embedder, cosine
from load import ThemeSet, rated_similarity_pairs


# --------------------------------------------------------------------------- #
# Embedding collection
# --------------------------------------------------------------------------- #
def all_texts(sets: dict[str, ThemeSet], comments: dict[str, str], rq: str) -> list[str]:
    """Every distinct text the analyses need embedded (for cost estimation)."""
    texts: list[str] = [rq, *comments.values()]
    for theme_set in sets.values():
        for theme in theme_set.rated_themes:
            texts.append(theme.embed_text(include_definition=True))
            texts.append(theme.embed_text(include_definition=False))
            texts.extend(q.text for q in theme.quotes if q.text)
    return texts


def build_vectors(
    sets: dict[str, ThemeSet], comments: dict[str, str], rq: str, embedder: Embedder
) -> dict[str, np.ndarray]:
    """Embed everything once and return a ``{text: vector}`` lookup."""
    return embedder.embed(all_texts(sets, comments, rq))


# --------------------------------------------------------------------------- #
# 1. Theme <-> research question
# --------------------------------------------------------------------------- #
def theme_rq_cosine(
    sets: dict[str, ThemeSet], vecs: dict[str, np.ndarray], rq: str
) -> pd.DataFrame:
    """Cosine of each theme to the research question, for both the name+definition
    representation and the name-only representation."""
    rq_vec = vecs[rq]
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        for theme in theme_set.rated_themes:
            rows.append(
                {
                    "condition": condition,
                    "theme": theme.name,
                    "cos_namedef_rq": cosine(vecs[theme.embed_text(True)], rq_vec),
                    "cos_nameonly_rq": cosine(vecs[theme.embed_text(False)], rq_vec),
                }
            )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 2. Quote-level distances (core vs supporting, interp level, quote vs data)
# --------------------------------------------------------------------------- #
def quote_level_table(
    sets: dict[str, ThemeSet], vecs: dict[str, np.ndarray], comments: dict[str, str]
) -> pd.DataFrame:
    """One row per quote.

    Columns:

    * ``cos_quote_theme``   - quote vs its theme (name+definition).
    * ``cos_quote_source``  - quote vs the comment it was drawn from (provenance;
      high is expected since the quote is an excerpt). ``NaN`` when unattributed.
    * ``mean_cos_corpus`` / ``max_cos_corpus`` - quote vs all comments
      (representativeness across the dataset).
    * ``nearest_comment`` / ``nearest_is_source`` - which comment the quote is
      closest to, and whether that is its claimed source.
    """
    comment_ids = list(comments)
    comment_vecs = [vecs[comments[cid]] for cid in comment_ids]
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        for theme in theme_set.rated_themes:
            theme_vec = vecs[theme.embed_text(True)]
            for quote in theme.quotes:
                if not quote.text:
                    continue
                qvec = vecs[quote.text]
                corpus_cos = [cosine(qvec, cv) for cv in comment_vecs]
                nearest_idx = int(np.argmax(corpus_cos))
                nearest_id = comment_ids[nearest_idx]
                source_cos = (
                    cosine(qvec, vecs[comments[quote.source]])
                    if quote.source in comments
                    else float("nan")
                )
                rows.append(
                    {
                        "condition": condition,
                        "theme": theme.name,
                        "role": quote.role,
                        "interp_level": theme.ratings.get("interpretationLevel"),
                        "source": quote.source,
                        "cos_quote_theme": cosine(qvec, theme_vec),
                        "cos_quote_source": source_cos,
                        "mean_cos_corpus": float(np.mean(corpus_cos)),
                        "max_cos_corpus": float(np.max(corpus_cos)),
                        "nearest_comment": nearest_id,
                        "nearest_is_source": (
                            None if quote.source is None else nearest_id == quote.source
                        ),
                    }
                )
    return pd.DataFrame(rows)


def core_vs_supporting(quote_df: pd.DataFrame) -> pd.DataFrame:
    """Per condition: mean quote-to-theme cosine split by role, and the gap.
    A positive ``core_minus_supporting`` means core quotes sit closer to the
    theme than supporting ones."""
    if quote_df.empty:
        return pd.DataFrame()
    wide = (
        quote_df.pivot_table(
            index="condition", columns="role", values="cos_quote_theme", aggfunc="mean"
        )
        .rename(columns={"core": "core_mean", "supporting": "supporting_mean"})
    )
    counts = quote_df.pivot_table(
        index="condition", columns="role", values="cos_quote_theme", aggfunc="count"
    ).rename(columns={"core": "n_core", "supporting": "n_supporting"})
    out = wide.join(counts)
    if "core_mean" in out and "supporting_mean" in out:
        out["core_minus_supporting"] = out["core_mean"] - out["supporting_mean"]
    return out.reset_index()


def interp_level_cosine(quote_df: pd.DataFrame) -> pd.DataFrame:
    """Mean quote-to-theme cosine grouped by the theme's interpretation level.
    The hypothesis: more interpretive themes (higher level) have quotes that sit
    farther from the theme text, i.e. a larger inferential gap (lower cosine)."""
    if quote_df.empty or quote_df["interp_level"].isna().all():
        return pd.DataFrame()
    grouped = (
        quote_df.dropna(subset=["interp_level"])
        .groupby("interp_level")["cos_quote_theme"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )
    return grouped


def interp_level_correlation(quote_df: pd.DataFrame) -> dict[str, float]:
    """Correlation between a theme's interpretation level and its quotes'
    distance from the theme. Negative => more interpretive, looser quotes."""
    valid = quote_df.dropna(subset=["interp_level", "cos_quote_theme"])
    if len(valid) < 3 or valid["interp_level"].nunique() < 2:
        return {"spearman": float("nan"), "pearson": float("nan"), "n": float(len(valid))}
    return {
        "spearman": float(valid["interp_level"].corr(valid["cos_quote_theme"], method="spearman")),
        "pearson": float(valid["interp_level"].corr(valid["cos_quote_theme"], method="pearson")),
        "n": float(len(valid)),
    }


# --------------------------------------------------------------------------- #
# 3. Theme <-> cited comments (grounding proxy; covers the low-effort condition)
# --------------------------------------------------------------------------- #
def theme_cited_cosine(
    sets: dict[str, ThemeSet], vecs: dict[str, np.ndarray], comments: dict[str, str]
) -> pd.DataFrame:
    """For each theme that cites comments, mean cosine to its cited comments vs
    to the rest of the corpus. ``cited_minus_other > 0`` means the theme embeds
    closer to the comments it claims to represent than to the others."""
    comment_ids = set(comments)
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        for theme in theme_set.rated_themes:
            cited = [c for c in theme.cited_sources if c in comment_ids]
            if not cited:
                continue
            theme_vec = vecs[theme.embed_text(True)]
            cited_set = set(cited)
            cited_cos = [cosine(theme_vec, vecs[comments[c]]) for c in cited]
            other_cos = [
                cosine(theme_vec, vecs[comments[c]]) for c in comment_ids if c not in cited_set
            ]
            mean_cited = float(np.mean(cited_cos))
            mean_other = float(np.mean(other_cos)) if other_cos else float("nan")
            rows.append(
                {
                    "condition": condition,
                    "theme": theme.name,
                    "n_cited": len(cited),
                    "mean_cos_cited": mean_cited,
                    "mean_cos_other": mean_other,
                    "cited_minus_other": mean_cited - mean_other,
                }
            )
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 4. Theme-pair similarity: embedding cosine vs human rating
# --------------------------------------------------------------------------- #
def theme_pairs(sets: dict[str, ThemeSet], vecs: dict[str, np.ndarray]) -> pd.DataFrame:
    """All within-condition unordered theme pairs with their embedding cosine and
    the human similarity rating where one exists (``NaN`` otherwise)."""
    rows: list[dict[str, object]] = []
    for condition, theme_set in sets.items():
        themes = theme_set.rated_themes
        human = {
            frozenset((a, b)): sim for a, b, sim, _ in rated_similarity_pairs(theme_set)
        }
        matched: set[frozenset[str]] = set()
        for i in range(len(themes)):
            for j in range(i + 1, len(themes)):
                a, b = themes[i], themes[j]
                key = frozenset((a.name, b.name))
                human_sim = human.get(key, float("nan"))
                if key in human:
                    matched.add(key)
                rows.append(
                    {
                        "condition": condition,
                        "theme_a": a.name,
                        "theme_b": b.name,
                        "cosine": cosine(vecs[a.embed_text(True)], vecs[b.embed_text(True)]),
                        "human_similarity": human_sim,
                        "rated": key in human,
                    }
                )
        # Surface any rated pair whose endpoints are not both rated themes.
        for key in set(human) - matched:
            a, b = sorted(key)
            rows.append(
                {
                    "condition": condition,
                    "theme_a": a,
                    "theme_b": b,
                    "cosine": float("nan"),
                    "human_similarity": human[key],
                    "rated": True,
                }
            )
    return pd.DataFrame(rows)


def similarity_validation(pairs_df: pd.DataFrame) -> pd.DataFrame:
    """Per condition: correlation between human similarity and embedding cosine
    over rated pairs, plus mean cosine for rated vs unrated pairs (does the
    implicit "unrated = independent" assumption hold?)."""
    rows: list[dict[str, object]] = []
    for condition, group in pairs_df.groupby("condition"):
        computable = group.dropna(subset=["cosine"])
        rated = computable[computable["rated"]]
        unrated = computable[~computable["rated"]]
        corr_pool = rated.dropna(subset=["human_similarity"])
        can_corr = len(corr_pool) >= 3 and corr_pool["human_similarity"].nunique() >= 2
        rows.append(
            {
                "condition": condition,
                "n_pairs": int(len(group)),
                "n_rated": int(group["rated"].sum()),
                "spearman": (
                    float(corr_pool["human_similarity"].corr(corr_pool["cosine"], method="spearman"))
                    if can_corr
                    else float("nan")
                ),
                "pearson": (
                    float(corr_pool["human_similarity"].corr(corr_pool["cosine"], method="pearson"))
                    if can_corr
                    else float("nan")
                ),
                "mean_cos_rated": float(rated["cosine"].mean()) if len(rated) else float("nan"),
                "mean_cos_unrated": float(unrated["cosine"].mean()) if len(unrated) else float("nan"),
                "max_cos_unrated": float(unrated["cosine"].max()) if len(unrated) else float("nan"),
            }
        )
    return pd.DataFrame(rows).set_index("condition")
