# Thematic-analysis summary — 20comments_v1

## Ratings by condition
Means over rated themes (non-null values per dimension). Scales are 1–5; for novelty/interpretation, higher = more novel / more interpretive.

| condition | n_themes | grounding | researchQuestionFit | interpretationLevel | aiPriorNovelty | analyticalNovelty | n_similarity_pairs | mean_similarity | mean_quotes_per_theme |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nodata | 20 | — | 4.75 | 2.35 | — | 2.20 | 10 | 3.10 | 0.00 |
| loweffort | 15 | 4.93 | 4.93 | 1.47 | 1.87 | 2.27 | 7 | 2.43 | 3.13 |
| engineered | 6 | 5.00 | 5.00 | 2.67 | 2.00 | 3.17 | 0 | — | 3.67 |
| human | 9 | 4.78 | 4.44 | 3.11 | 3.88 | 3.33 | 0 | — | 21.33 |

## Theme ↔ research question (cosine)
How close each condition's themes sit to the RQ, on average.

| condition | mean_cos_namedef_rq | mean_cos_nameonly_rq |
| --- | --- | --- |
| engineered | 0.584 | 0.478 |
| human | 0.597 | 0.429 |
| loweffort | 0.513 | 0.341 |
| nodata | 0.533 | 0.368 |

## Core vs supporting quotes (cosine to theme)
`core_minus_supporting` > 0 means core quotes sit closer to the theme.

| condition | core_mean | supporting_mean | n_core | n_supporting | core_minus_supporting |
| --- | --- | --- | --- | --- | --- |
| engineered | 0.597 | 0.517 | 11.000 | 11.000 | 0.080 |
| human | 0.325 | 0.352 | 122.000 | 70.000 | -0.027 |
| loweffort | — | 0.421 | — | 47.000 | — |

## Interpretation level ↔ quote distance
Correlation of a theme's interpretation level with its quote→theme cosine (n=214): Spearman **0.201**, Pearson **0.138**. Negative ⇒ more interpretive themes have looser (less similar) quotes.

## Human similarity vs embedding cosine
Does embedding cosine reproduce the 1–5 theme-similarity ratings, and are unrated (implicitly independent) pairs actually lower-cosine than rated ones?

| condition | n_pairs | n_rated | spearman | pearson | mean_cos_rated | mean_cos_unrated | max_cos_unrated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| engineered | 15 | 0 | — | — | — | 0.631 | 0.746 |
| human | 36 | 0 | — | — | — | 0.632 | 0.747 |
| loweffort | 105 | 7 | -0.089 | 0.015 | 0.612 | 0.515 | 0.706 |
| nodata | 190 | 10 | 0.770 | 0.661 | 0.624 | 0.513 | 0.717 |

## Caveats
- **no-data**: themes are model priors with no data, so there are no quotes; `grounding` and `aiPriorNovelty` are not applicable (shown as `—`).
- **low-effort**: quotes are model paraphrases without verbatim source ids, so quote-to-source provenance is unavailable; the condition instead cites comments inside each definition (`Representative comments: D..`), which drive its theme-to-cited-comment grounding signal.
- **human**: the analysis is hierarchical; the 9 rated subthemes are the unit of analysis and the 2 parent/container nodes (all-null ratings) are excluded.
- Theme-similarity ratings exist only where pairs crossed the rating threshold (no-data, low-effort). Unrated pairs are treated as implicitly independent and checked against their embedding cosine.
