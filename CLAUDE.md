# CLAUDE.md — Agent Instructions

Rules for any Claude Code session working on this project.

---

## Before You Start

- Read `README.md` for folder structure and output naming conventions.
- Read `PRD.md` to understand what the project is for.
- Read `ARCHITECTURE.md` to understand how the system and project is built as well as what the code does.
- If a task is ambiguous about where something goes or how it interacts with existing work — ask before implementing. THIS IS VERY IMPORTANT

---

## After Every Change

- If you changed computation logic, data flow, or pipeline structure: update `ARCHITECTURE.md`.
- If you added, removed, or changed a research component or evaluation element: update `PRD.md`.
- If there are instructions all Claude Code sessions should follow: update `CLAUDE.md`.
- If changes touch folder structure, naming conventions, or project setup: update `README.md`.
- Make sure each of these `ARCHITECTURE.md`, `PRD.md`, `CLAUDE.md`, and `README.md` files are a reasonable length - long enough for needed details but not more than that.
- Make sure to match the styling for writing in all of these md files when you edit.

---

## Git Workflow

- Never commit OR push without asking first. Always confirm with the user before doing so.
- Commit messages must be detailed. One-line summaries are not enough — explain *why* the change was made, what problem it solves, or what it enables.
- Stage changes thoughtfully based on what was changed 

---

## Prompt Development Workflow

When a prompt is edited and ready to be logged as a new version:

1. Rename the prompt file: `engineered_v1.md` → `engineered_v2.md` (increment version)
2. Update PROMPTS_LOG.md:
   - Copy the new version into the log under a new `### Version X` header
   - Bold the changed sections
   - Add the template rationale under the changed section for the user to fill in

---

## Code Quality

- Use type hints on all function signatures.
- Keep functions focused — if a function does multiple unrelated things, split it.
- Prefer small, targeted edits over full file rewrites.

---

## Guardrails

(None yet — add pitfalls and failure modes here as they are discovered during implementation.)
