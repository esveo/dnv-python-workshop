---
name: new-analysis
description: Adds a new analysis to grid_analysis. Use when someone asks for a new check, count or calculation on nodes or lines.
---

1. Clarify what is unclear before writing code: inputs and outputs with units, and what happens exactly on a limit.
2. Write the tests first in `tests/test_domain.py`: the normal case, each limit, the empty list. One test per case.
3. Implement the analysis as a pure function in `src/grid_analysis/domain.py`. It receives `Node` or `Line` objects as parameters and returns a value.
4. Use the existing constants (`MIN_VOLTAGE_PU`, `MAX_VOLTAGE_PU`, `MAX_LOADING_PERCENT`) as defaults instead of new numbers.
5. Write the docstring in NumPy style with the unit of every parameter and of the return value.
6. Run `uv run ruff check`, `uv run mypy src` and `uv run pytest` and fix what they report.
