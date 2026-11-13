# Python workshop: exercise project `grid_analysis`

The exercise project for the Python workshop. The full course content (topics, explanations and exercises per session) is in [`workshop/README.md`](workshop/README.md). It is modelled on typical PowerFactory evaluations: a load flow is run, then node voltages and line loadings are checked and printed as a report.

You do not need a PowerFactory licence. The module `powerfactory_fake` mimics the most important parts of the real Python API (`GetApplication`, `GetFromStudyCase("ComLdf")`, `GetCalcRelevantObjects`, `GetAttribute("m:u")`, `GetAttribute("c:loading")`). The code looks like a real script but runs on any machine.

## Preparation

An overview of all tools, grouped by how they are installed. Each one is explained when it first comes up in the workshop.

**Install in advance**

| Tool | What for | Installation |
| --- | --- | --- |
| [VS Code](https://code.visualstudio.com/) | Editor (alternatively Visual Studio) | Installer |
| [GitHub Copilot](https://docs.github.com/en/copilot) | AI assistant in the editor | Already included in VS Code; sign in with a GitHub account that has a Copilot licence |
| [Git](https://git-scm.com/) | Version control | Installer (Git for Windows) |
| [uv](https://docs.astral.sh/uv/) | Manages Python versions, environments and packages | One PowerShell command, see below; no preinstalled Python required |

Install uv (PowerShell), any one of the three ways is enough:

```powershell
# Ideal for managed environments
pip install uv

# Standard method (downloads an install script from astral.sh)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative via the Windows package manager
winget install --id=astral-sh.uv -e
```

**Installed in the project by uv (comes later)**

You do not have to install these yourself. They are listed in `pyproject.toml`, and `uv sync` installs all of them at once. uv also downloads Python itself if necessary.

| Tool | What for |
| --- | --- |
| Python | Interpreter; the project specifies the version |
| [Ruff](https://docs.astral.sh/ruff/) | Linter and formatter |
| [mypy](https://mypy.readthedocs.io/) | Type checker |
| [Bandit](https://bandit.readthedocs.io/) | Offline security analysis of your own code |
| [pytest](https://docs.pytest.org/), [pytest-cov](https://pytest-cov.readthedocs.io/) | Write and run tests, measure coverage |
| [NumPy](https://numpy.org/), [SciPy](https://scipy.org/) | Array calculations and scientific methods |
| [Sphinx](https://www.sphinx-doc.org/) | Generate documentation from code |
| [Nuitka](https://nuitka.net/), [PyInstaller](https://pyinstaller.org/), [Cython](https://cython.org/) | Compiling and bundling (reserve session) |

**Separate (only if needed, reserve session)**

| Tool | What for | Installation |
| --- | --- | --- |
| [Snyk CLI](https://docs.snyk.io/developer-tools/snyk-cli) | Security analysis of dependencies and code | Separate program, not through Python: download as an `.exe`, or use npm or the Snyk extension for VS Code |
| Visual Studio Build Tools | C compiler for Nuitka and Cython | Microsoft installer |

### 💪 Check your tools

Before the workshop starts, make sure the following are available:

- Open **VS Code**.
- In the Extensions view (View > Extensions), check that the **Python** extension by Microsoft is installed.
- Open a terminal and run `python --version` (or `py --version` on Windows) to check the **Python CLI**; this should be your globally installed version.
- Run `uv --version` to check **uv**. If it is missing, install it using one of the methods above.
- Run `git --version` to check the **Git CLI**.

If a check fails, let the trainer know.

### Python version and PowerFactory

- For the workshop, the Python version does not matter: uv installs the version the project specifies in `requires-python` or `.python-version` into `.venv`.
- For real scripts it does matter, see [From the fake to the real PowerFactory](#from-the-fake-to-the-real-powerfactory).

### Prerequisites

The workshop builds on Python basics that are not explained separately:

- Variables, data types (`int`, `float`, `str`, `bool`), lists and dictionaries
- `if`, `for`, functions with parameters and default values, `return`
- List comprehensions (`[n for n in nodes if ...]`)
- Classes with `__init__` and methods, creating objects
- Importing modules (`import`, `from ... import ...`)
- Exceptions (`raise`, `try`/`except`)
- `with` blocks (e.g. when opening files)
- Opening a terminal, changing folders with `cd` and running commands

## Quick start

```powershell
git clone https://github.com/esveo/dnv-python-workshop.git
cd dnv-python-workshop
uv sync
uv run python -m grid_analysis
```

The last command prints a short report. `uv run python -m grid_analysis peak-load` or `light-load` evaluates a different scenario.

## The most important commands

| Command | What it does |
| --- | --- |
| `uv sync` | Recreates the environment exactly as pinned in `uv.lock` |
| `uv run python -m grid_analysis` | Runs the program |
| `uv run pytest` | Runs the tests |
| `uv run pytest --cov=grid_analysis --cov-report=term-missing` | Tests with coverage |
| `uv run ruff check` | Linting (`--fix` repairs simple cases) |
| `uv run ruff format` | Formats the code |
| `uv run mypy src` | Checks the type hints |
| `uv run bandit -r src` | Security check of your own code |

## Project structure

```txt
dnv-python-workshop/
├── pyproject.toml           # metadata, dependencies, tool configuration
├── uv.lock                  # exact versions of all packages
├── src/grid_analysis/
│   ├── __main__.py          # entry point for python -m grid_analysis
│   ├── domain.py            # checks and calculations (domain logic)
│   ├── data_source.py       # the only place with access to PowerFactory
│   ├── report.py            # output
│   └── powerfactory_fake.py # stand-in for the PowerFactory API
├── exercises/               # one task per exercise
├── workshop/                # course content per session
└── tests/
```

Project rules (`AGENTS.md`) and skills (`.agents/skills/`) are missing on purpose: you create them in exercise 05.

## Domain terms

- **Voltage in p.u. (per unit):** voltage relative to the nominal voltage, 1.0 equals 100 %.
- **Voltage band:** the permitted range, 0.95 to 1.05 p.u. in this project. The limits belong to the band. Below it is undervoltage, above it overvoltage.
- **Loading:** how heavily a line is loaded, in percent. From 100 % on, the project treats a line as overloaded.
- **Scenario:** an operating state of the grid, e.g. peak load or light load.

`Node` and `Line` are small data classes with a name and a measured value, e.g. `Line("L1", 80.0)`. `data_source.py` translates the PowerFactory objects into these classes.

## Exercises

Every exercise has a folder under `exercises/` with a `README.md`: the task, hints and the criteria for "done". The exercises build on each other and all run in this repository.

**Session 1: Fundamentals**

| No. | Exercise | Topic |
| --- | --- | --- |
| 01 | [Set up and push a project](exercises/01/README.md) | Git and project structure with uv |
| 02 | [Fix findings](exercises/02/README.md) | Code quality and static analysis |
| 03 | [Write your first tests yourself](exercises/03/README.md) | Unit tests, TDD |
| 04 | [AI writes tests, you review them](exercises/04/README.md) | Unit tests with AI |

**Session 2: Maintainable code with AI**

| No. | Exercise | Topic |
| --- | --- | --- |
| 05 | [Set up project rules and skills](exercises/05/README.md) | Project rules, skills and MCP |
| 06 | [Separate domain logic from the data source](exercises/06/README.md) | Pure functions and inversion of control |
| 07 | [From loops to arrays](exercises/07/README.md) | NumPy and performance |
| 08 | [From specification to finished module](exercises/08/README.md) | Planning, agent, review |

**Reserve session**

| No. | Exercise | Topic |
| --- | --- | --- |
| R1 | [A module as .pyd, the program as .exe](exercises/R1/README.md) | Compiling |
| R2 | [Calculate scenarios in parallel](exercises/R2/README.md) | Parallelisation |
| R3 | [Sphinx for your own project](exercises/R3/README.md) | API documentation |
| R4 | [Create and resolve a conflict](exercises/R4/README.md) | Git conflicts |
| R5 | [Find a vulnerability](exercises/R5/README.md) | Snyk |

The starting code contains bugs and style problems on purpose. They are part of exercises 02 and 03.

## Rules for working with AI

- Formulate your own idea for a solution first, then ask
- Do not adopt anything you cannot explain
- Let the AI explain, not just do ("Why is that?")
- AI code without tests is unverified code

## Sample solutions

The sample solutions will be provided after the sessions.

## From the fake to the real PowerFactory

Access to PowerFactory lives only in `src/grid_analysis/data_source.py`. In real use the import there changes, e.g. for PowerFactory 2024 with Python 3.12:

```py
import sys

sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12")
import powerfactory
```

The `powerfactory` module is compiled and ships in a separate folder of the PowerFactory installation for each supported Python version (e.g. `...\PowerFactory 2026\Python\3.13`). The Python version of the project has to match one of these folders. Pin it with uv, e.g. `uv python pin 3.13`.
