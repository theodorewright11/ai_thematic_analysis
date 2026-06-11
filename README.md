# AI Thematic Analysis

Systematic thematic analysis of user comments using different LLM prompting strategies.

## Project Structure

```
ai_thematic_analysis/
├── README.md
├── prompts/
│   └── themes/
│       ├── engineered_v1.md
│       ├── loweffort_v1.md
│       └── nodata_v1.md
├── data/
│   ├── comments_20.csv
│   └── comments_160.csv (later)
├── outputs/
│   └── themes/
│       ├── chatgpt_engineered_v1_20_run1.json
│       ├── chatgpt_loweffort_v1_20_run1.json
│       ├── chatgpt_nodata_v1_run1.json
│       ├── claude_engineered_v1_20_run1.json
│       └── ...
└── scripts/ (later)
```

## Naming Conventions

### Output Files
Format: `{model}_{promptvariant}_v{version}_{datasize}_run{n}.json`

- **model**: `chatgpt`, `claude`, `gemini`
- **promptvariant**: `engineered`, `loweffort`, `nodata`
- **version**: `v1`, `v2` (increments when prompt changes)
- **datasize**: `20`, `160` (omitted for `nodata`)
- **run**: `run1`, `run2` (for consistency measurement)

### Prompt Files
Format: `{variant}_v{version}.md`

Examples:
- `engineered_v1.md`
- `loweffort_v2.md`
- `nodata_v1.md`

## Authors and Affiliations

<!-- Add author info and paper citation here -->
