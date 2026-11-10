---
name: check-solution
description: Checks the solution of an exercise. Use when someone asks whether an exercise is finished or correct.
---

1. Run `uv run ruff check`, `uv run mypy src` and `uv run pytest`.
2. Read the task in `exercises/<number>/README.md` and check every criterion individually.
3. For every criterion, report met / not met with a short reason.
4. Do not give away a solution. For open points, only give a hint where to look.
