# ARCHITECTURE.md — How It Works

How the analysis is built and what the code does. For *why*, see `PRD.md`.

---

## Data flow

```
data/comments_20.md              outputs/ratings/themes/*.themes-ratings.json
  (corpus: [Dn] text)              (one human-rated themeset per condition)
        |                                       |
        +------------------+--------------------+
                           v
                   scripts/ (typed, reusable)
        load -> metrics -> embed -> embed_analysis -> report
                           v
                  analysis/results/<RUN_NAME>/
                  summary.md  ·  detailed.md  ·  *.csv
```

`analysis/run_analysis.ipynb` is the runner: a CONFIG cell (data file, rating
files, research question, embedding model, run name) plus one cell per stage, so
the same pipeline runs on a new dataset by editing config only.

---

## Conditions

Four themesets are compared. They differ in what is computable:

| Condition  | Themes           | Quotes                     | Notes |
|------------|------------------|----------------------------|-------|
| no-data    | model priors     | none                       | `grounding`, `aiPriorNovelty` are N/A |
| low-effort | minimal prompt   | paraphrased, unattributed  | cites comments in the definition (`Representative comments: D..`) |
| engineered | developed prompt | verbatim + source id       | full provenance |
| human      | reference (teddy)| verbatim + source id       | hierarchical; the rated subthemes are the unit of analysis |

---

## Scripts

- **load.py** — parses the `[Dn]` corpus and each rating file into typed
  `Theme` / `Quote` / `SimilarityLink` records. A node is a *theme* only if it
  carries at least one non-null rating (drops the human parent containers).
  Accepts `quotes` or `supporting` for the quote array; treats a `source` of
  `"N/A.."` as unattributed; extracts `Dn` ids cited in definitions.
- **metrics.py** — per-condition rating aggregates (means over non-null values).
- **embed.py** — `text-embedding-3-large` client with a sha256 on-disk cache
  (`analysis/cache/`) and cosine helpers. The API key is read from `.env` only
  when an actual embedding call is needed, so ratings run without a key.
- **embed_analysis.py** — the cosine analyses (below).
- **report.py** — renders CSVs + `summary.md` (mentor) + `detailed.md` (reference).

---

## Embedding analyses

A theme is represented by *name + definition*; all similarities are cosine.

1. **Theme ↔ RQ** — each theme vs the research question.
2. **Quote level** — quote vs theme (split by core/supporting role and by the
   theme's interpretation level), quote vs its source comment (provenance), and
   quote vs the whole corpus (representativeness).
3. **Theme ↔ cited comments** — does a theme embed closer to the comments it
   cites than to the rest (grounding proxy; the only quote-free signal for
   low-effort, whose definitions cite `Dn` ids).
4. **Similarity validation** — within-condition theme-pair cosine vs the human
   1–5 similarity ratings (correlation), and rated vs unrated pair cosines (does
   "unrated = independent" hold?).
