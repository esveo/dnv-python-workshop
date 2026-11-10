# Sample solutions

One folder per exercise with the state after that exercise. Try it yourself first, then compare.

## How the folders are organised

Files sit under the same path as in the project:

```txt
solutions/03/src/grid_analysis/domain.py   ->  src/grid_analysis/domain.py
solutions/03/tests/test_domain.py          ->  tests/test_domain.py
```

The solutions build on each other: the files in `solutions/05/` contain everything from exercises 02 to 05. A folder only contains the files that the exercise changes. For a file that is missing, take it from the closest earlier folder.

Every folder has a `README.md` that explains the solution.

## Catching up

If you are stuck and want to continue with the next exercise, copy the files of the last finished exercise over your project. Example for the state after exercise 03 (PowerShell):

```powershell
Copy-Item -Recurse -Force solutions\02\src, solutions\03\src, solutions\03\tests .
```

Also add the Ruff rule sets from exercise 02 to `pyproject.toml`:

```toml
[tool.ruff.lint]
extend-select = ["B", "I", "N"]
```

## Overview

| Exercise | Contents |
| --- | --- |
| [01](01/README.md) | Commands step by step |
| [02](02/README.md) | Fixed findings in `domain.py`, `report.py`, `data_source.py` |
| [03](03/README.md) | Tests for `within_voltage_band`, bug fix, `is_overloaded` |
| [04](04/README.md) | Tests for `overloaded_lines` |
| [05](05/README.md) | `AGENTS.md`, both skills, the two counting functions |
| [06](06/README.md) | Refactoring into core and shell, test with a fake data source |
| [07](07/README.md) | Vectorised version with broadcasting, tests |
| [08](08/README.md) | Specification, module `loading_summary.py`, tests |
| [R1](R1/README.md) | Commands and expected results |
| [R2](R2/README.md) | Parallel version with measurements |
| [R3](R3/README.md) | `docs/conf.py`, `docs/index.rst`, docstring examples |
| [R4](R4/README.md) | Commands step by step |
| [R5](R5/README.md) | The vulnerable package and the update |
