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

### Per-Theme Ratings (5-point scales)

**Grounding**: Is this theme accurately based in the data? Evaluates whether the theme reflects real patterns in the dataset, whether supporting evidence supports the claims, and whether interpretive bridges from data to theme are traceable and convincing.

**RQ-Fit**: Does this theme serve the research question at the specificity and depth it demands? Evaluates whether the theme addresses what the RQ asks for at an appropriate level of analysis.

### Per-Theme Descriptor (5-point scale)

**Interpretation Level**: How far beyond the surface text does this theme go? Documents the degree of inference involved. Descriptive, not evaluative — higher interpretation is not inherently better or worse.

### Computed Metrics

**Novelty**: Cosine similarity between each with-data theme and its nearest match in the no-data baseline output. Measures how much the dataset contributed versus model priors.

**Prevalence**: Fraction of data items a theme touches, computed from quote assignments.

### Set-Level Assessments

**Coverage**: Count of themes passing a quality threshold.

**Independence**: Pairwise cosine similarity between theme definitions. Overlapping themes flagged for merging. Applied as a filter during set construction.

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
