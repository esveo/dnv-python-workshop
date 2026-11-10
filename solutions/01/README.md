# Solution 01: Set up a project and push it

## Part 1

```powershell
git init --bare C:\git-exercise\grid-analysis.git
cd C:\git-exercise
git clone C:\git-exercise\grid-analysis.git
cd grid-analysis

uv init --package
uv add numpy
uv add --dev pytest ruff mypy

git status
git add .
git commit -m "Set up project with uv"
git push -u origin main
```

Afterwards `pyproject.toml` looks roughly like this (the version numbers will differ):

```toml
[project]
name = "grid-analysis"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "numpy>=2.1",
]

[dependency-groups]
dev = [
    "mypy>=1.13",
    "pytest>=8",
    "ruff>=0.8",
]
```

What `uv` did:

- `uv init --package` created `pyproject.toml`, `src/grid_analysis/__init__.py`, `.python-version`, `.gitignore` and `README.md`
- `uv add` entered the packages in `pyproject.toml`, wrote the exact versions to `uv.lock` and installed them into `.venv`

The `.gitignore` created by `uv init` already covers `.venv` and `__pycache__/`. Missing by the rule of thumb, depending on what you use later: coverage reports (`.coverage`, `htmlcov/`), generated documentation (`docs/_build/`), tool caches (`.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`) and compiled files (`*.pyd`, `*.exe`). Compare with the `.gitignore` of the exercise repository.

If the branch is called `master` instead of `main`: `git branch -m main` renames it, `git config --global init.defaultBranch main` sets the default for new repositories.

## Part 2

```powershell
git clone https://github.com/esveo/dnv-python-workshop.git
cd dnv-python-workshop
uv sync
uv run python -m grid_analysis
```

Expected output:

```txt
Grid analysis North Grid
========================

Nodes: 8, mean voltage: 0.987 p.u.
Within voltage band: 88 %
Lines: 6

Voltage band violations (0.95 to 1.05 p.u.):
  BUS South             0.943 p.u.

Overloaded lines (from 100 %):
  L4 Station-Plant         104.2 %

Overloaded: L4 Station-Plant
```
