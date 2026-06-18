"""Render analysis tables to CSVs and two markdown reports.

* ``summary.md``  - mentor-facing: a few clean headline tables + caveats.
* ``detailed.md`` - reference: every per-theme / per-pair table.

This module only formats; all numbers come from :mod:`metrics` and
:mod:`embed_analysis`. Embedding sections are skipped gracefully when their
tables are empty (e.g. a ratings-only run before any API key is set).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

CAVEATS: list[str] = [
    "**no-data**: themes are model priors with no data, so there are no quotes; "
    "`grounding` and `aiPriorNovelty` are not applicable (shown as `—`).",
    "**low-effort**: quotes are model paraphrases without verbatim source ids, so "
    "quote-to-source provenance is unavailable; the condition instead cites comments "
    "inside each definition (`Representative comments: D..`), which drive its "
    "theme-to-cited-comment grounding signal.",
    "**human**: the analysis is hierarchical; the 9 rated subthemes are the unit of "
    "analysis and the 2 parent/container nodes (all-null ratings) are excluded.",
    "Theme-similarity ratings exist only where pairs crossed the rating threshold "
    "(no-data, low-effort). Unrated pairs are treated as implicitly independent and "
    "checked against their embedding cosine.",
]


# --------------------------------------------------------------------------- #
# Formatting helpers
# --------------------------------------------------------------------------- #
def _fmt(value: object, floatfmt: str) -> str:
    if isinstance(value, float):
        return "—" if np.isnan(value) else floatfmt.format(value)
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return str(value)


def md_table(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    """GitHub-flavored markdown table from a DataFrame (named index becomes a
    leading column)."""
    if df is None or df.empty:
        return "_(no rows)_"
    table = df.reset_index() if df.index.name else df.copy()
    cols = [str(c) for c in table.columns]
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in table.iterrows():
        lines.append("| " + " | ".join(_fmt(row[c], floatfmt) for c in table.columns) + " |")
    return "\n".join(lines)


def write_csvs(output_dir: str | Path, tables: dict[str, pd.DataFrame]) -> list[str]:
    """Write each non-empty table to ``output_dir/<name>.csv``."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for name, df in tables.items():
        if df is None or df.empty:
            continue
        path = out / f"{name}.csv"
        df.to_csv(path, index=bool(df.index.name))
        written.append(str(path))
    return written


# --------------------------------------------------------------------------- #
# Presentation aggregations
# --------------------------------------------------------------------------- #
def _rq_by_condition(rq_df: pd.DataFrame) -> pd.DataFrame:
    return (
        rq_df.groupby("condition")[["cos_namedef_rq", "cos_nameonly_rq"]]
        .mean()
        .rename(columns={"cos_namedef_rq": "mean_cos_namedef_rq", "cos_nameonly_rq": "mean_cos_nameonly_rq"})
    )


def _quote_by_condition(quote_df: pd.DataFrame) -> pd.DataFrame:
    return quote_df.groupby("condition").agg(
        n_quotes=("cos_quote_theme", "count"),
        mean_quote_theme=("cos_quote_theme", "mean"),
        mean_quote_source=("cos_quote_source", "mean"),
        mean_quote_corpus=("mean_cos_corpus", "mean"),
    )


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #
def build_summary_md(
    *,
    run_name: str,
    rating_tbl: pd.DataFrame,
    rq_df: pd.DataFrame | None = None,
    core_supp: pd.DataFrame | None = None,
    interp_corr: dict[str, float] | None = None,
    sim_val: pd.DataFrame | None = None,
) -> str:
    parts: list[str] = [
        f"# Thematic-analysis summary — {run_name}",
        "",
        "## Ratings by condition",
        "Means over rated themes (non-null values per dimension). Scales are 1–5; "
        "for novelty/interpretation, higher = more novel / more interpretive.",
        "",
        md_table(rating_tbl, floatfmt="{:.2f}"),
    ]
    if rq_df is not None and not rq_df.empty:
        parts += [
            "",
            "## Theme ↔ research question (cosine)",
            "How close each condition's themes sit to the RQ, on average.",
            "",
            md_table(_rq_by_condition(rq_df)),
        ]
    if core_supp is not None and not core_supp.empty:
        parts += [
            "",
            "## Core vs supporting quotes (cosine to theme)",
            "`core_minus_supporting` > 0 means core quotes sit closer to the theme.",
            "",
            md_table(core_supp),
        ]
    if interp_corr is not None and not np.isnan(interp_corr.get("spearman", float("nan"))):
        parts += [
            "",
            "## Interpretation level ↔ quote distance",
            f"Correlation of a theme's interpretation level with its quote→theme cosine "
            f"(n={int(interp_corr['n'])}): Spearman **{interp_corr['spearman']:.3f}**, "
            f"Pearson **{interp_corr['pearson']:.3f}**. "
            "Negative ⇒ more interpretive themes have looser (less similar) quotes.",
        ]
    if sim_val is not None and not sim_val.empty:
        parts += [
            "",
            "## Human similarity vs embedding cosine",
            "Does embedding cosine reproduce the 1–5 theme-similarity ratings, and are "
            "unrated (implicitly independent) pairs actually lower-cosine than rated ones?",
            "",
            md_table(sim_val),
        ]
    parts += ["", "## Caveats", *[f"- {c}" for c in CAVEATS], ""]
    return "\n".join(parts)


def build_detailed_md(
    *,
    run_name: str,
    rating_tbl: pd.DataFrame,
    theme_ratings: pd.DataFrame,
    rq_df: pd.DataFrame | None = None,
    quote_df: pd.DataFrame | None = None,
    interp_level: pd.DataFrame | None = None,
    theme_cited: pd.DataFrame | None = None,
    pairs_df: pd.DataFrame | None = None,
    sim_val: pd.DataFrame | None = None,
) -> str:
    parts: list[str] = [
        f"# Thematic-analysis detail — {run_name}",
        "",
        "## Ratings by condition",
        md_table(rating_tbl, floatfmt="{:.2f}"),
        "",
        "## Per-theme ratings",
        md_table(theme_ratings, floatfmt="{:.0f}"),
    ]
    if rq_df is not None and not rq_df.empty:
        parts += ["", "## Per-theme cosine to research question", md_table(rq_df)]
    if quote_df is not None and not quote_df.empty:
        parts += [
            "",
            "## Quote-level distances, summarized by condition",
            "`mean_quote_source` is provenance (quote vs its origin comment); "
            "`mean_quote_corpus` is representativeness (quote vs all comments).",
            "",
            md_table(_quote_by_condition(quote_df)),
        ]
    if interp_level is not None and not interp_level.empty:
        parts += [
            "",
            "## Quote→theme cosine by interpretation level",
            md_table(interp_level),
        ]
    if theme_cited is not None and not theme_cited.empty:
        parts += [
            "",
            "## Theme ↔ cited comments (grounding proxy)",
            "`cited_minus_other` > 0 means the theme embeds closer to the comments it "
            "cites than to the rest of the corpus.",
            "",
            md_table(theme_cited),
        ]
    if pairs_df is not None and not pairs_df.empty:
        rated_pairs = pairs_df[pairs_df["rated"]].sort_values("human_similarity", ascending=False)
        if not rated_pairs.empty:
            parts += ["", "## Rated theme pairs (human similarity vs cosine)", md_table(rated_pairs)]
        top_unrated = (
            pairs_df[~pairs_df["rated"]].dropna(subset=["cosine"]).nlargest(15, "cosine")
        )
        if not top_unrated.empty:
            parts += [
                "",
                "## Highest-cosine unrated pairs (independence check)",
                "If implicit independence holds, even the closest unrated pairs stay "
                "well below the rated ones.",
                "",
                md_table(top_unrated),
            ]
    if sim_val is not None and not sim_val.empty:
        parts += ["", "## Similarity validation", md_table(sim_val)]
    parts += ["", "## Caveats", *[f"- {c}" for c in CAVEATS], ""]
    return "\n".join(parts)


def write_reports(output_dir: str | Path, run_name: str, tables: dict[str, object]) -> dict[str, list[str]]:
    """Write CSVs + summary.md + detailed.md. ``tables`` holds the analysis
    outputs by name; missing/empty ones are skipped."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    csv_tables = {k: v for k, v in tables.items() if isinstance(v, pd.DataFrame)}
    csv_paths = write_csvs(out, csv_tables)

    summary = build_summary_md(
        run_name=run_name,
        rating_tbl=tables["rating_tbl"],
        rq_df=tables.get("rq_df"),
        core_supp=tables.get("core_supp"),
        interp_corr=tables.get("interp_corr"),
        sim_val=tables.get("sim_val"),
    )
    detailed = build_detailed_md(
        run_name=run_name,
        rating_tbl=tables["rating_tbl"],
        theme_ratings=tables["theme_ratings"],
        rq_df=tables.get("rq_df"),
        quote_df=tables.get("quote_df"),
        interp_level=tables.get("interp_level"),
        theme_cited=tables.get("theme_cited"),
        pairs_df=tables.get("pairs_df"),
        sim_val=tables.get("sim_val"),
    )
    (out / "summary.md").write_text(summary, encoding="utf-8")
    (out / "detailed.md").write_text(detailed, encoding="utf-8")
    return {"csvs": csv_paths, "reports": [str(out / "summary.md"), str(out / "detailed.md")]}
