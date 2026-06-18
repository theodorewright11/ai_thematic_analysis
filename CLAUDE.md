# CLAUDE.md — Agent Instructions

Rules for any Claude Code session working on this project.

---

## Before You Start

- Read `README.md` for folder structure and output naming conventions.
- Read `PRD.md` to understand what the project is for.
- Read `ARCHITECTURE.md` to understand how the system and project is built as well as what the code does.
- If a task is ambiguous about where something goes or how it interacts with existing work — ask before implementing. THIS IS VERY IMPORTANT. For most tasks default to asking the user before making any changes.

---

## After Every Change

- If you changed computation logic, data flow, or pipeline structure: update `ARCHITECTURE.md`.
- If you added, removed, or changed a research component or evaluation element: update `PRD.md`.
- If there are instructions all Claude Code sessions should follow: update `CLAUDE.md`.
- If changes touch folder structure, naming conventions, or project setup: update `README.md`.
- Keep `ARCHITECTURE.md`, `PRD.md`, `CLAUDE.md`, and `README.md` lean and tight — long enough for the important details, never bloated. Trim as you add; do not leave anything important out.
- Make sure to match the styling for writing in all of these md files when you edit.

---

## Git Workflow

- Never commit OR push without asking first. Always confirm with the user before doing so.
- Commit messages must be detailed. One-line summaries are not enough — explain *why* the change was made, what problem it solves, or what it enables.
- Stage changes thoughtfully based on what was changed 

---

## Prompt Development Workflow

The user edits a prompt and renames the file (`engineered_v1.md` → `engineered_v2.md`), then asks to log it. When asked:

1. Add a new `### Version X` block to PROMPTS_LOG.md with the full new prompt text and the changed sections **bolded**. The user typically will not have the rationale yet — they use the bolded changes to write it.
2. Later, when the user provides the rationale bullets, fill them into that version's block (they supply the *why* — do not invent it).

Do not commit/push as part of this — the user reviews first, then approves committing per the Git Workflow rules. Prior versions are never lost: exact content stays in git history, and readable copies stay in PROMPTS_LOG.md.

---

## Code Quality

- Use type hints on all function signatures.
- Keep functions focused — if a function does multiple unrelated things, split it.
- Prefer small, targeted edits over full file rewrites.

---

## Guardrails

- The rated exports in `outputs/ratings/themes/*.themes-ratings.json` are the canonical data for analysis. A node is a *theme* only if it has ≥1 non-null rating — this drops the human set's parent/container nodes.
- The quote array may be named `quotes` or `supporting` (renamed mid-project); the loader accepts both. A quote `source` of `"N/A.."` means unattributed.
- Conditions are asymmetric — do not assume a field exists everywhere: no-data has no quotes and N/A `grounding`/`aiPriorNovelty`; low-effort quotes are paraphrased and cite comments inside the definition; only engineered/human have verbatim sourced quotes.
- Analysis code in `scripts/` is generic and dataset-agnostic; experiment-specific values live only in the `analysis/run_analysis.ipynb` CONFIG cell. Keep it that way.
