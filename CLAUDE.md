# CLAUDE.md — Agent Instructions

Rules for any Claude Code session working on this project.

---

## Before You Start

- Read `PRD.md` to understand what the project is for.
- Read `ARCHITECTURE.md` to understand how the system and project is built as well as what the code does.
- If a task is ambiguous about where something goes or how it interacts with existing work — ask before implementing. THIS IS VERY IMPORTANT

---

## After Every Change

- If you changed computation logic, data flow, or pipeline structure: update `ARCHITECTURE.md`.
- If you added, removed, or changed a research component or evaluation element: update `PRD.md`.
- If there are instructions all Claude Code sessions should follow: update `CLAUDE.md`.
- Make sure each of these `ARCHITECTURE.md`, `PRD.md`, and `CLAUDE.md` files are a reasonable length - long enough for needed details but not more than that.

---

## Code Quality

- Use type hints on all function signatures.
- Keep functions focused — if a function does multiple unrelated things, split it.
- Prefer small, targeted edits over full file rewrites.

---

## Guardrails

(None yet — add pitfalls and failure modes here as they are discovered during implementation.)
