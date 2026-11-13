---
name: check-solution
description: Checks an exercise solution. Use when someone asks whether an exercise is complete or correct.
---

1. Run `uv run ruff check`, `uv run mypy src` and `uv run pytest`.
2. Read the task in `exercises/<number>/README.md` and check each criterion individually.
3. Report met / not met for each criterion with a brief explanation.
4. Do not reveal the solution. For unresolved points, only hint where to look.
