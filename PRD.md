# PRD.md — What This Project Is

---

## Purpose

This project investigates how AI performs thematic analysis (TA) of qualitative data — what the output looks like, what controls its quality, and what AI adds to the process that wasn't previously practical.

TA takes qualitative data (comments, interviews, transcripts) and produces themes that capture meaningful patterns relevant to a research question. This has traditionally been done entirely by human researchers. LLMs can now generate thematic outputs from the same data. This project produces empirical evidence and a reusable evaluation framework for understanding AI's role in this process.

The empirical context is public comments submitted to the FDA by the ALS patient community regarding drug development policy. Human analyses of these comments exist as reference points for comparison.

---

## Team

| Role | Department | Contribution |
|------|-----------|-------------|
| Undergraduate researcher | Computing (Kahlert School), U of U | Primary researcher — methodology design, prompt engineering, evaluation framework, empirical runs, analysis, writing |
| Faculty supervisor (primary) | Computing / HCI, U of U | Research direction, HCI framing, mentorship |
| Faculty co-supervisor | Communication, U of U | Qualitative methods expertise, domain knowledge |
| Graduate collaborator | Computing / HCI , U of U | Expert on ALS comment data; prior human thematic analysis serves as reference standard |

---

## Evaluation Framework

Themes are rated by hand on 1–5 scales, then probed with embeddings. Some
dimensions do not apply in every condition (e.g. grounding is meaningless with no
data) — see `ARCHITECTURE.md`.

### Per-Theme Ratings (evaluative, 1–5)

**Grounding**: Does the theme accurately reflect patterns in the data — do the extracts demonstrate it, and are interpretive bridges from extract to theme traceable and convincing?

**RQ-Fit**: Does the theme advance the analysis at the specificity and depth the research question demands?

### Per-Theme Descriptors (1–5, not better/worse)

**Interpretation Level**: How far beyond the surface text the theme goes.

**AI Prior Novelty**: Whether the theme's subject appears in the no-data baseline (model priors).

**Analytical Novelty**: Whether domain familiarity alone would anticipate the theme without reading the data.

### Set-Level Assessments

**Independence**: Pairwise **Theme Similarity** (1–5) rated by hand; pairs below threshold are left unrated and treated as implicitly independent. Overlapping themes are flagged for merging.

**Coverage**: Count of themes passing a quality threshold.

### Computed Metrics (embeddings — `text-embedding-3-large`)

**Theme–RQ alignment**, a **grounding proxy** (theme/quote vs the comments it draws on; quote provenance vs corpus representativeness), **core-vs-supporting separation**, **interpretation level vs quote distance**, and **similarity validation** (does embedding cosine reproduce the human Theme Similarity ratings, so independence can scale). **Prevalence** (quote coverage of data items) is planned.

---

## Research Question Topology

Research questions vary on two dimensions that affect what kind of TA output is appropriate:

**Specificity**: How constrained the analytical territory is. Open ("what are people experiencing") to focused ("what specific trial design changes are recommended").

**Depth**: What level of analytical complexity the RQ demands. Surface content patterns to deep interpretive claims about dynamics, relationships, and contextual functions.

AI performance varies across this space. Mapping that variation is a central empirical goal.

---

## Data

| Dataset | Size | Role |
|---------|------|------|
| 20-comment test set | 20 public comments | Primary test bed for prompt iteration, evaluation calibration, and rapid comparison |
| 162-comment full set | 162 public comments | Full dataset for scaled runs once methodology is established |

Both are public comments from regulations.gov on FDA ALS drug development guidance.

---

## Experimental Conditions

### Baseline conditions
- **No data**: AI generates predicted themes from priors only
- **Low-effort**: Comments provided with minimal prompt
- **Engineered**: Comments provided with the developed prompt

### Prompt variables (tested by varying one at a time)
- RQ specificity and depth variants
- Mathematical language vs. natural language
- Rich domain context vs. minimal context
- Instructed interpretation vs. uninstructed
- Prediction framing vs. expert role-play framing
- One-shot example vs. none
- Direction specificity

### Models
- Claude, ChatGPT, Gemini — multiple tiers per provider where relevant
- Same model re-runs for determinism metrics
