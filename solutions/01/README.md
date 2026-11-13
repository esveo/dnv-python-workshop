# Solution 01: Set up and push a project

## Part 1

```powershell
git init --bare C:\git-exercise\grid_analysis.git
cd C:\git-exercise
git clone C:\git-exercise\grid_analysis.git
cd grid_analysis

uv init --package --python 3.13
uv add numpy
uv add --dev pytest ruff mypy

# create .gitignore (see below)

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
requires-python = ">=3.13"
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

- `uv init --package --python 3.13` created `pyproject.toml`, `src/grid_analysis/__init__.py`, `.python-version` (with `3.13`) and `README.md`. uv normalises the project name in `pyproject.toml` to `grid-analysis`; the package folder stays `grid_analysis`.
- `uv add` entered the packages in `pyproject.toml`, wrote the exact versions to `uv.lock` and installed them into `.venv`

Because the folder is already a Git repository (the clone), `uv init` does not create a `.gitignore`. Create it yourself. A minimal version following the rule of thumb:

```txt
# Virtual environment and files Python generates itself
.venv/
__pycache__/
*.py[cod]

# Tool caches
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Coverage reports
.coverage
htmlcov/

# Build results and generated documentation
build/
dist/
*.pyd
*.exe
docs/_build/
```

Alternatively start from a ready-made one, e.g. the one from the [uv template](https://github.com/python-boilerplate/uv-template/blob/main/.gitignore), or compare with the `.gitignore` of the exercise repository. Check with `git status` before committing: `.venv/` must not show up, `uv.lock`, `.python-version` and `.gitignore` must.

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
