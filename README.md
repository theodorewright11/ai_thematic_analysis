# AI Thematic Analysis

Systematic thematic analysis of user comments using different LLM prompting strategies.

## Project Structure

```
ai_thematic_analysis/
├── README.md · PRD.md · ARCHITECTURE.md · CLAUDE.md
├── prompts/
│   ├── PROMPTS_LOG.md          # full text + rationale per prompt version
│   ├── themes/                 # engineered_v2.md, loweffort_v1.md, nodata_v1.md
│   └── other/
├── data/                       # comments_20.md ([Dn] corpus) + comments_20.csv
├── outputs/
│   ├── ai/themes/              # raw model theme outputs (.json/.md)
│   └── ratings/themes/         # human-rated themesets (.themes-ratings.json)
├── scripts/                    # load · embed · metrics · embed_analysis · report
└── analysis/
    ├── run_analysis.ipynb      # runner (edit CONFIG, run top-to-bottom)
    ├── cache/                  # embeddings cache (gitignored)
    └── results/<run_name>/     # summary.md · detailed.md · *.csv
```

## Naming Conventions

### Model theme outputs — `outputs/ai/themes/`
`{model}_{promptvariant}_v{version}_{datasize}_run{n}.json`

- **model**: `chatgpt5.5`, `claude`, `gemini`
- **promptvariant**: `engineered`, `loweffort`, `nodata`
- **version**: `v1`, `v2` (increments when the prompt changes)
- **datasize**: `20`, `160` (omitted for `nodata`)
- **run**: `run1`, `run2` (consistency measurement)

### Rated themesets — `outputs/ratings/themes/`
The matching output stem plus `.themes-ratings.json` (the rated export of an output),
paired with a `.themes-ratings.md` readable view (the same data rendered with an
at-a-glance ratings table). The human reference set carries its author in the model slot:
`human_teddy_v1_20_run1.themes-ratings.json`.

### Prompt files — `prompts/themes/`
`{variant}_v{version}.md` (e.g. `engineered_v2.md`). Evolution + rationale live in
`prompts/PROMPTS_LOG.md`.

## Running the Analysis

1. Create/activate the venv, then `pip install -r requirements-dev.txt`.
2. Copy `.env.example` → `.env` and set `OPENAI_API_KEY` (only the embedding steps need it).
3. Open `analysis/run_analysis.ipynb`, edit the **CONFIG** cell, and run top-to-bottom.
   Sections 1–2 (load + ratings) need no key; sections 3–5 (embeddings) do.

See `ARCHITECTURE.md` for the pipeline and `PRD.md` for the research goals.

## Authors and Affiliations

<!-- Add author info and paper citation here -->
