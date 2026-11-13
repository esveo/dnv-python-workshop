# Python workshop: course content

The content of the workshop: two four-hour sessions plus an optional reserve session. AI fundamentals come early so that the later exercises can be done with AI support. The exercise tasks themselves are in [`exercises/`](../exercises/), the setup in the [main README](../README.md).

Each exercise has two parts: first you solve the key point yourself, then AI builds on your work and you review the result.

## Schedule

### Session 1: Fundamentals (4 h)

| Topic | Min | Exercise |
| --- | --- | --- |
| Introduction and setup check | 20 |  |
| Git and project structure with uv | 60 | 💪 01 |
| AI fundamentals | 35 |  |
| Break | 15 |  |
| Code quality and static analysis | 35 | 💪 02 |
| Unit tests | 65 | 💪 03, 💪 04 |
| Session 1 wrap-up | 10 |  |

### Session 2: Maintainable code with AI (4 h)

| Topic | Min | Exercise |
| --- | --- | --- |
| Recap | 10 |  |
| Project rules, skills and MCP | 50 | 💪 05 |
| Pure functions and inversion of control | 55 | 💪 06 |
| Break | 15 |  |
| NumPy and performance | 45 | 💪 07 |
| Planning, agent and review | 45 | 💪 08 |
| API documentation (demo), feedback | 20 |  |

**Reserve session (4 h, another day):** Compiling to `.pyd` and `.exe`, parallelization, an API documentation exercise, Git conflicts, and hands-on Snyk. It also provides time for anything that takes longer than planned in sessions 1 and 2.

## Session 1: Fundamentals

### Introduction

**Who are you?**

- Name and experience with Python
- What are you currently working on?
- Expectations for the training

**Before we start**

- Be curious and open-minded
- Questions are welcome at any time
- We use AI from the beginning, but with clear rules

**Our editor: VS Code**

- A free code editor from Microsoft, with extensions for almost any language
- Important for the training: the Python extension (running, debugging, test view), the Git view, the integrated terminal and GitHub Copilot
- The terminal opens at the bottom of the editor (Terminal > New Terminal) and starts in the project folder
- Setup check: everyone opens the exercise project, the terminal and Copilot Chat

### Preparation

An overview of all tools, grouped by how they are installed. Each is explained in more detail when first introduced in a session.

**Install in advance**

| Tool | Purpose | Installation | Explained in |
| --- | --- | --- | --- |
| [VS Code](https://code.visualstudio.com/) | Editor (alternatively Visual Studio) | Installer | Introduction |
| [GitHub Copilot](https://docs.github.com/en/copilot) | AI assistant in the editor | Already included in VS Code; sign in with a GitHub account that has a Copilot license | AI fundamentals |
| [Git](https://git-scm.com/) | Version control | Installer (Git for Windows) | Git and project structure |
| [uv](https://docs.astral.sh/uv/) | Manage Python versions, environments and packages | One PowerShell command; no preinstalled Python required | Git and project structure |

**Installed in the project by uv (coming later)**

These are listed in the exercise project's `pyproject.toml`; `uv sync` installs everything at once. uv also downloads Python itself if necessary.

| Tool | Purpose | Explained in |
| --- | --- | --- |
| Python | Interpreter; the project specifies the version | Git and project structure |
| [Ruff](https://docs.astral.sh/ruff/) | Linter and formatter | Code quality |
| [mypy](https://mypy.readthedocs.io/) | Type checker | Code quality |
| [Bandit](https://bandit.readthedocs.io/) | Offline security analysis of your own code | Code quality |
| [pytest](https://docs.pytest.org/), [pytest-cov](https://pytest-cov.readthedocs.io/) | Write and run tests, measure coverage | Unit tests |
| [NumPy](https://numpy.org/), [SciPy](https://scipy.org/) | Array calculations and scientific methods | NumPy and performance |
| [Sphinx](https://www.sphinx-doc.org/) | Generate documentation from code | API documentation |
| [Nuitka](https://nuitka.net/), [PyInstaller](https://pyinstaller.org/), [Cython](https://cython.org/) | Compiling and bundling | Reserve session |

**Separate (only if needed)**

| Tool | Purpose | Installation | Explained in |
| --- | --- | --- | --- |
| [Snyk CLI](https://docs.snyk.io/developer-tools/snyk-cli) | Security analysis of dependencies and code | Separate program, not through Python: download as an `.exe`, or use npm or the Snyk extension for VS Code | Code quality, reserve session |
| Visual Studio Build Tools | C compiler for Nuitka and Cython | Microsoft installer | Reserve session |

#### 💪 Check your tools

Before starting, make sure the following are available:

- Open **VS Code**.
- In the Extensions view (View > Extensions), check that the **Python** extension by Microsoft is installed.
- Open a terminal and run `python --version` (or `py --version` on Windows) to check the **Python CLI**; this should be your globally installed version.
- Run `uv --version` to check **uv**. If it is missing, install it using one of the methods below.
- Run `git --version` to check the **Git CLI**.

If a check fails, let the trainer know.

**Installing uv**

```powershell
# Ideal for managed environments
pip install uv

# Standard method (downloads an installation script from astral.sh)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative using the Windows package manager
winget install --id=astral-sh.uv -e
```

#### Summary

**Python version and PowerFactory**

- For the training, the Python version does not matter: uv installs the version specified by the project in `requires-python` or `.python-version` into `.venv`
- For real scripts it does matter: the `powerfactory` module is compiled and is located in a separate folder in the PowerFactory installation for each supported Python version (e.g. `...\PowerFactory 2026\Python\3.13`). The environment’s Python version must match one of these folders.

**Prerequisites**

The training builds on Python basics that we do not explain separately:

- Variables, data types (`int`, `float`, `str`, `bool`), lists and dictionaries
- `if`, `for`, functions with parameters and default values, `return`
- List comprehensions (`[n for n in nodes if ...]`)
- Classes with `__init__` and methods, creating objects
- Importing modules (`import`, `from ... import ...`)
- Exceptions (`raise`, `try`/`except`)
- `with` blocks (e.g. when opening files)
- Opening a terminal, changing folders with `cd` and running commands

### Exercise project

**What PowerFactory scripts look like**

PowerFactory comes with a Python module called `powerfactory`. Scripts run either inside PowerFactory itself (as a Python command in the project) or externally, in which case PowerFactory starts in the background (“Engine Mode”). A typical script:

```py
import sys
sys.path.append(r"C:\Program Files\DIgSILENT\PowerFactory 2024\Python\3.12")
import powerfactory

app = powerfactory.GetApplication()
app.ActivateProject("North Grid")

ldf = app.GetFromStudyCase("ComLdf")  # load-flow command
ldf.Execute()

for node in app.GetCalcRelevantObjects("*.ElmTerm"):  # all nodes
    u = node.GetAttribute("m:u")  # voltage in p.u.
    if u < 0.95 or u > 1.05:
        app.PrintPlain(f"{node.loc_name}: {u:.3f} p.u.")

for line in app.GetCalcRelevantObjects("*.ElmLne"):  # all lines
    if line.GetAttribute("c:loading") > 100:  # loading in %
        app.PrintPlain(f"{line.loc_name} overloaded")
```

- Typical of scripts that have grown over time: a long sequence without functions, limits as numbers in the code, output mixed with domain logic, executable only with a PowerFactory license and therefore not testable
- We refactor precisely these points step by step during the training

**Exercise project `grid_analysis`**

Based on typical PowerFactory analyses. We provide it as a ready-made Git repository, which participants clone in exercise 01.

- A fake module `powerfactory_fake` mirrors the most important parts of the real API (`GetApplication`, `GetFromStudyCase("ComLdf")`, `GetCalcRelevantObjects`, `GetAttribute("m:u")`, `GetAttribute("c:loading")`). It also provides several scenarios and large test datasets for the performance exercise.
- Everything runs without a license while the code still looks like a real PowerFactory script. In real use, only the import in `data_source.py` changes.
- `Node` and `Line` are small data classes with a name and measurement, e.g. `Line("L1", 80.0)`. `data_source.py` translates PowerFactory objects into these classes.
- Domain terminology:
  - Voltage in p.u. (per unit): voltage relative to nominal voltage; 1.0 equals 100%
  - Voltage band: permitted range, 0.95 to 1.05 p.u. in the project. Below this is undervoltage; above it is overvoltage.
  - Line loading as a percentage; above 100% the line is overloaded
- `python -m grid_analysis` produces a short report (via `__main__.py`)

```txt
grid_analysis/
├── pyproject.toml
├── uv.lock
├── src/grid_analysis/
│   ├── __main__.py          # entry point for python -m grid_analysis
│   ├── domain.py            # checks and calculations
│   ├── data_source.py       # only place accessing PowerFactory
│   ├── report.py            # output
│   └── powerfactory_fake.py # replica of the PowerFactory API
├── exercises/               # exercise tasks
├── solutions/               # sample solutions, will be provided later
└── tests/
```

Project rules (`AGENTS.md`) and skills (`.agents/skills/`) are created in exercise 05.

### Git and project structure with uv

**Git**

This is a high-level introduction to Git that covers what is needed for the exercises. Git comes first because everything else goes into the repository.

- Git is a version control system: it stores a project's history. You can see who changed what, when and why, and return to any previous state.
- Repository: the project folder together with its entire history (stored in the hidden `.git` subfolder)
- Commit: a saved state of the project with a message explaining why. Before committing, use `git add` to stage the changes to include.
- Remote: another copy of the repository with which you exchange commits, usually a shared location for the team
- Cloning: fetching a complete copy of a repository and its history to your computer. The clone remembers its source, automatically configured as the remote named `origin`.
- A folder or network drive can be used as a remote; a Git server is not strictly necessary. A bare repository is a repository without a working directory, used only as shared storage.
- Branch: a development line. `main` is the main branch. In the main sessions we work only on `main`; multiple branches are covered in the reserve session.

```txt
main      ●───●───────────────●   Merge: changes back into main
               \             /
feature         ●─────●─────●     separate branch for a new feature
```

**Basic Git commands**

- `git init --bare <path>`: creates an empty bare repository as shared storage
- `git clone <path>`: clones the repository into a new folder
- `git status`: shows what has changed and what is staged
- `git add <file>`: stages changes for the next commit
- `git commit -m "Message"`: saves the staged changes as a commit
- `git push` / `git pull`: send commits to or fetch them from the remote
- First push to an empty remote: `git push -u origin main`. `-u` links the local branch with the remote; afterwards `git push` is enough.
- All of this can also be done through the editor's Git view

**Python project terminology**

- Package: reusable Python code to install, e.g. NumPy. Packages usually come from [PyPI](https://pypi.org/), the central package index for Python.
- Dependency: a package the project needs to run
- Virtual environment: a folder with its own Python installation and packages for each project. Projects with different versions do not get in one another’s way.

**What is uv?**

- A command-line tool from Astral (the company behind Ruff) that manages Python projects
- It replaces several older tools at once: `pip` (install packages), `venv` (create environments), `pip-tools` (lock versions) and `pyenv` (install Python versions)
- Why uv: one tool instead of four, considerably faster, and the lock file guarantees everyone the same environment
- uv needs no preinstalled Python. It is installed once per computer and then downloads the appropriate Python version for each project itself.

**Project structure**

- `src` layout: code in `src/<package>/`, tests in `tests/`
- Split modules by domain responsibility. Keep domain logic, data access and tests separate.
- `pyproject.toml`: metadata, runtime and development dependencies, and tool configuration in one file
- The file uses TOML: sections in square brackets (`[project]`) followed by entries in the form `key = value`
- Dependency versions: `numpy>=2.1` means “version 2.1 or newer.” The exact installed version is in the lock file.
- Lock file `uv.lock`: exact versions of all packages
- Virtual environment `.venv`: the project's own Python installation and packages; it can be recreated from `uv.lock` at any time

**uv in everyday use**

- `uv init --package`: turns the current folder into a project with `pyproject.toml` and a `src` layout. With a name (`uv init --package <name>`), uv creates a new subfolder instead.
- `uv add <package>`: installs a runtime dependency. uv adds it to `pyproject.toml`, updates `uv.lock` and installs it in `.venv`.
- `uv add --dev <package>`: the same for development tools not needed to run the application. Here these include pytest, Ruff and mypy, explained in the next sections.
- `uv remove <package>`: removes a package
- `uv sync`: recreates the environment exactly from `uv.lock`, e.g. after cloning
- `uv run <command>`: runs a command in the project environment without needing to activate it first, e.g. `uv run python -m grid_analysis`
- `uv python pin <version>`: sets the project's Python version (important for PowerFactory; see preparation)
- `uv run python -m <package>` starts a package as a program. Python runs the package's `__main__.py` file.

```toml
[project]
name = "grid_analysis"
requires-python = ">=3.12"
dependencies = ["numpy>=2.1"]

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.8", "mypy>=1.13"]
```

**What belongs in the repository?**

Rule of thumb: include everything written by hand and needed to recreate the project on another computer. Ignore anything that can be generated automatically, applies only to one computer or is secret.

- ✅ Include: source code, tests, `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`, documentation, project rules and skills
- ❌ Ignore: `.venv/`, `__pycache__/` (intermediate files generated by Python), build artifacts (`build/`, `dist/`, `.pyd`, `.exe`), coverage reports and generated documentation (`docs/_build/`)
- ❌ Never include: passwords, credentials, license files or real customer network data
- `.gitignore`: list of files and folders Git ignores. `uv init` already creates a suitable one.
  - There are also ready-made `.gitignore` files, e.g. the one from the [uv template](https://github.com/python-boilerplate/uv-template/blob/main/.gitignore)

#### 💪 01 Set up and push a project

**Part 1**

- Create a bare repository as a “server” and clone it:

```powershell
git init --bare C:\git-exercise\grid_analysis.git
git clone C:\git-exercise\grid_analysis.git
```

- Enter the clone (`cd grid_analysis`) and turn it into a project: `uv init --package --python 3.13`
- Add NumPy (`uv add numpy`) and pytest, Ruff and mypy as development dependencies
- Look at what changed in `pyproject.toml`
- Create a `.gitignore` file
- Commit and push (first push with `git push -u origin main`)

**Part 2**

- Clone the exercise repository from the path we give you into your own folder
- Set up the environment: `uv sync`
- Check that everything runs: `uv run python -m grid_analysis` prints a short report
- From here on, all exercises use this exercise repository

#### Summary and notes

- Git manages source code, no matter the language
- uv can be used to manage our python project, with dependencies, packages, versions and more

**Note on using Git with other ways of sharing code, such as OneDrive or network shares:** Set up the remote on the share itself with `git init --bare \\server\path\to\project.git`. Limitations of a network drive: it shares versions but offers no pull requests or automated tests. Never put a bare repository in a synchronized folder (OneDrive, SharePoint); the sync client can damage the files in `.git` . A known stumbling block is the ownership check (“dubious ownership”), addressed via `git config --global --add safe.directory`. A real Git server such as Bitbucket, GitHub or Azure DevOps is the better choice where available.

**More:** [uv: projects](https://docs.astral.sh/uv/guides/projects/) · [uv: installation](https://docs.astral.sh/uv/getting-started/installation/) · [src vs. flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) · [Learn Git Branching](https://learngitbranching.js.org/) · [Pro Git: Git on the server](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server)

### AI fundamentals

- A large language model (LLM) is an AI model trained on vast amounts of text and code. It predicts the most likely next piece of a word (token). Plausible does not mean correct.
- GitHub Copilot is an AI assistant from GitHub (owned by Microsoft) that works directly in the editor. It sends the code around the current position to a language model and displays the response. Using it requires a Copilot license.
- Copilot has three ways of working: autocomplete while typing, chat for questions, and agent mode for autonomous tasks (covered in session 2)
- Prompt: the request you write to the AI

**What models are available?**

Copilot is not a model itself; it offers models from several providers: Claude (Anthropic), GPT (OpenAI), Gemini (Google) and others. GitHub divides them into three classes (prices as of November 2026). Since June 2026, Copilot bills according to tokens consumed; output is more expensive than input.

| Class | Examples | Price per 1 million tokens (input / output) | Uses |
| --- | --- | --- | --- |
| Lightweight | GPT-6 Luna, Claude Haiku 5.5 | approx. \$0.10 / \$0.50 | Autocomplete, routine work, short questions |
| Versatile | Claude Sonnet 5.5, GPT-6.1 Terra, Gemini 3.8 Flash | approx. \$0.75–2 / \$3.75–10 | Everyday coding, agent mode |
| Powerful | Claude Opus 5.5, GPT-6.1 Sol, Gemini 4 Argon, top models such as GPT-6 Astra | approx. \$2–10 / \$10–50 | Planning, difficult bugs, major refactoring |

- Powerful models are often “reasoning” models: they work through intermediate steps before answering, making them slower and more expensive
- Rule of thumb: start with a versatile model; switch to a powerful one only for planning and difficult cases
- Your organization’s license determines which models are available and how much budget is provided

**Two terms we will use constantly**

- Type hints: annotations describing the types of parameters and return values (`voltage_pu: float`, `-> bool`). Python itself does not check them at runtime; they provide information to people, tools and AI. `list[Node]` means “list of Node objects.”
- Docstring: the text in triple quotation marks directly below `def`. It describes what the function does. The editor, documentation tools and AI read it too.

```py
def within_voltage_band(voltage_pu: float, min_pu: float = 0.95, max_pu: float = 1.05) -> bool:
    """Checks whether a node voltage is within the permitted band.

    Voltages are in p.u. (per unit); the limits are included.
    """
```

- Autocomplete: write the signature, type hints and docstring first, then read and check the suggestion
- Chat: ask for code explanations, targeted questions and small changes to selected sections
- Suggestions are most dangerous when they are almost correct

**Pros and cons**

- ✅ Faster for routine work: repetitive boilerplate, tests, renaming, documentation
- ✅ Helpful for explaining unfamiliar code and libraries
- ❌ Confidently produces incorrect code, especially for numerical work and edge cases
- ❌ If you only prompt, you will not learn to program
- ❌ Data privacy: what may be included in a prompt?
- ❌ Cost: powerful models consume the budget quickly

**Rules for this training (and afterwards)**

- First formulate your own solution idea, then ask
- Do not accept anything you cannot explain
- Ask AI to explain, not just to do (“Why is it like that?”)
- AI code without tests is unverified code (we cover how to write tests at the end of session 1)

**Live demo:** Write a docstring, let autocomplete suggest the function, ask about an edge case in chat and find the error in the suggestion.

**More:** [Supported models in Copilot](https://docs.github.com/en/copilot/reference/ai-models/supported-models) · [GitHub model comparison](https://docs.github.com/en/copilot/reference/ai-models/model-comparison) · [Tips for good prompts](https://www.promptingguide.ai/introduction/tips)

### Code quality and static analysis

- PEPs (Python Enhancement Proposals) are official documents through which Python evolves. PEP 8 is the style guide: names, indentation, line length, imports.
- PEP 8 provides a common language; a tool enforces it
- Static analysis means checking code without executing it. Three types of tools:
  - Formatter: automatically gives code a consistent style, eliminating style debates
  - Linter: finds suspicious places and common errors, e.g. unused variables or dangerous default arguments
  - Type checker: checks whether type hints fit together, e.g. whether a function expecting `float` is given a `str`

**Our tools**

- Ruff: linter and formatter in one, from Astral (like uv). Replaces older tools such as flake8, black and isort and is very fast. Runs offline.
- mypy: the most widely used Python type checker. Runs offline.
- Bandit: looks for insecure patterns in your own code, e.g. `eval()` (executes arbitrary text as code), passwords in code or unsafe system-command calls. Runs offline. Install with `uv add --dev bandit`; run with `uv run bandit -r src`
- Snyk: commercial security service. Checks dependencies against a database of known vulnerabilities and scans your own code for insecure patterns. A separate program (not installable via uv), it requires an account and a connection to the Snyk service, so it does not run offline. We can try Snyk in the reserve session.

**Running and configuring tools**

- `uv run ruff check`: linting; `uv run ruff check --fix` fixes simple cases automatically
- `uv run ruff format`: formats the code
- `uv run mypy src`: checks type hints
- Ruff is organized into rule sets, each with a prefix. By default only a basic selection from `E` and `F` is active (major errors). Enable others in `pyproject.toml`:
  - `B` (Bugbear): common error sources such as mutable default arguments
  - `I`: import sorting
  - `N`: PEP 8 naming conventions
- Each finding has a code (e.g. `B006`) under which Ruff's documentation explains why the rule exists

```toml
[tool.ruff.lint]
extend-select = ["B", "I", "N"]
```

**Most important: names and constants**

In engineering calculations, formulas made of single-letter names and bare numbers quickly become difficult to understand. No tool can solve this for us.

- ✅ Descriptive names, units in names (`voltage_pu`, `current_a`, `loading_percent`)
- ✅ Named constants instead of “magic numbers,” i.e. unnamed numbers embedded in code (`MAX_LOADING_PERCENT = 100` instead of `100`)
- ✅ Do not type physical constants by hand: use `math.pi`, `math.sqrt(3)` or `scipy.constants`

```py
# Hard to read: what is 1.732? Which units?
def p(u, i, x):
    return 1.732 * u * i * x / 1000

# Readable: formula, units and constant are visible
SQRT_3 = math.sqrt(3)

def three_phase_active_power_kw(voltage_v: float, current_a: float, power_factor: float) -> float:
    """Active power in a three-phase network: P = √3 · U · I · cos φ."""
    return SQRT_3 * voltage_v * current_a * power_factor / 1000
```

**Other dos and don'ts**

- ✅ Small functions with one responsibility; as a rule of thumb, at most 1.5–2 screens
- ✅ Type hints on all functions used by other modules
- ❌ Global state: module-level variables modified by functions. It becomes impossible to see who changed what and when.
- ❌ A bare `except:` without an exception type: catches every error, including typos, and hides it
- ❌ Mutable default arguments such as `def f(values=[])`: the list is created only once and shared by all calls
- ❌ Commented-out code: old versions are in Git

#### 💪 02 Fix findings

**Part 1 (without AI)**

- Run `uv run ruff check` and `uv run mypy src` in the exercise repository
- Enable Ruff rule sets `B`, `I` and `N` in `pyproject.toml`
- Fix the first three findings yourself
- Install the Ruff extension and turn on format on save
  - In a Python file, open the command palette with Ctrl+Shift+P
  - Search for “Format Document With” and select “Configure Default Formatter”
  - Select Ruff
  - Open the settings by searching “Open Settings (UI)” in the command palette
  - Turn on “Format On Save”
  - Edit a file and save it to format it

**Part 2 (with AI)**

- Ask Copilot to explain why the rule exists for two more findings and have it fix them
- Which findings were actual bugs and which were only style?
- `domain.py` contains a function with single-letter names and magic numbers: rename it descriptively together with Copilot

**More:** [PEP 8](https://peps.python.org/pep-0008/) · [Code Smells](https://refactoring.guru/refactoring/smells) · [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html) · [Snyk: uv support](https://docs.snyk.io/supported-languages/supported-languages-list/python/cli-support-for-uv)

### Unit tests

- Tests are a safety net: they give you confidence to change code and make AI-generated code verifiable
- Unit test: checks a small unit, usually a function, in isolation and quickly
- A test has three steps: Arrange (prepare inputs), Act (call the function), Assert (check the result)
- pytest is the most widely used Python test framework. Python includes `unittest`, but pytest requires much less code.
- In pytest, tests are ordinary functions with `assert`: if the condition is false, the test fails
- pytest automatically finds tests in files named `test_*.py` and functions named `test_*`
- Run `uv run pytest` in the terminal or use the editor's test view. A failed test shows the expected and actual values.
- One test per case, with a name describing the case. This is enough for almost everything.
- Floating-point numbers are not exact: `0.1 + 0.2` produces `0.30000000000000004`. Therefore, never compare with `==`; use a tolerance: `assert result == pytest.approx(0.3)`
- Special case `NaN` (“not a number”, e.g. a missing measurement): create it with `float("nan")`. Every comparison with `NaN` is `False`, including `NaN == NaN`. Check with `math.isnan()`.
- Test what matters to the domain: edge cases and behavior, not every line
- Are my tests any good? Deliberately introduce an error: at least one test must fail.
- Coverage shows untested areas. 100% does not mean error-free.
- Measure coverage with pytest-cov, a pytest plugin: install with `uv add --dev pytest-cov`, then run `uv run pytest --cov=grid_analysis --cov-report=term-missing` (shows untested line numbers)
- Just for reference: fixtures and parametrization (`@pytest.mark.parametrize`) are available for many similar cases. We do not need them in the training.

```py
from grid_analysis.domain import within_voltage_band

def test_nominal_voltage_is_within_the_band():
    assert within_voltage_band(1.00)

def test_lower_limit_still_belongs_to_the_band():
    assert within_voltage_band(0.95)

def test_undervoltage_is_outside_the_band():
    assert not within_voltage_band(0.94)
```

**Test-driven development (TDD)**

- Write the test first, then the implementation
- Three-step cycle: Red (write a failing test), Green (implement just enough to make it pass), Refactor (clean up while tests stay green)
- Advantage: you must first clarify exactly what the function should do, including edge cases
- Works well with AI: the tests are the specification. AI can implement; the tests decide whether it is correct.

#### 💪 03 Write your first tests yourself (without AI)

**Part 1**

- Open `src/grid_analysis/domain.py` and `tests/test_domain.py`
- Write tests for `within_voltage_band(voltage_pu: float) -> bool`: inside, outside, exactly on the limits, `NaN`
- One test fails because the implementation has a boundary bug. Find and fix it.

**Part 2 (TDD)**

- First write tests for a new function `is_overloaded(loading_percent: float, limit_percent: float = 100) -> bool`
- Make them fail, then implement the function until all tests pass

#### 💪 04 AI writes tests, you review them

**Part 1**

- Ask Copilot Chat to write tests for `overloaded_lines(lines, limit_percent)` from `domain.py` and add them to `tests/test_domain.py`
- Review: do the tests check behavior or merely reproduce the implementation? Are edge cases missing?

**Part 2**

- Deliberately introduce a bug into the function (e.g. `>` instead of `>=`). Do the tests catch it?
- Add the missing tests yourself
- View coverage: `uv run pytest --cov=grid_analysis --cov-report=term-missing`

**More:** [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/) · [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) · [Test-Driven Development (Martin Fowler)](https://martinfowler.com/bliki/TestDrivenDevelopment.html) · [Stop Vibe Coding Your Unit Tests](https://www.andy-gallagher.com/blog/stop-vibe-coding-your-unit-tests/)

### Session 1 wrap-up

- Short summary of what we covered today
  - Git
  - Python project with uv
  - Copilot
  - Code quality
  - Unit tests
- Open questions
- What was new or unclear?
- Preview of session 2

## Session 2: Maintainable code with AI

### Recap

- Quick round: what do you remember from session 1? Has anyone tried anything since then?

### Project rules, skills and MCP

**Agent mode in brief**

- Copilot Chat has several modes. In Ask mode, Copilot answers questions. In agent mode, it works autonomously: it reads files, changes multiple files and executes terminal commands.
- Every command is shown for confirmation before execution
- File changes appear as a diff to accept or reject. A diff compares old and new versions line by line: removed lines in red, new lines in green.
- Skills and MCP work only in agent mode
- How to plan larger tasks with agents is covered later in this session

**Why does AI start from scratch every time?**

- A language model has no memory. To the model, every request is new.
- What looks like memory is text sent along with the request: the context. Copilot assembles it anew for each request:
  - System prompt: fixed instructions from Copilot itself (role, rules, available tools)
  - Project rules from the repository
  - Open or selected files
  - Previous chat history
  - The new question
- Continuing a chat means the entire previous history is sent again. A new chat starts empty.
- Context has a maximum size (context window). Long chats are truncated or summarized, quality drops and costs rise. Therefore: new task, new chat.
- Without rules, AI guesses your conventions anew in every session

**Project rules**

- Project rules are a short Markdown file (`.md`) containing structure, commands, conventions and prohibitions. Markdown is a simple text format: `#` at the beginning of a line for headings, `-` for lists, code in backticks ( `uv run pytest` ).
- Technically this is text Copilot automatically attaches to every request, like an extended system prompt. Keep it short: every line takes up space in each request.
- The file lives in the repository and is versioned with Git, so the same rules apply to everyone
- We use `AGENTS.md` in the project folder: an open standard read by Copilot and many other AI tools
- The alternative `.github/copilot-instructions.md` works only with Copilot

**Skills**

- Skills: instructions for recurring workflows in the repository
- Location: one folder per skill under `.agents/skills/`, containing a `SKILL.md` file
- File header, between two lines of `---`: `name` and `description`. AI initially sees only the description and loads the skill when it matches the task. The description should therefore say when the skill should be used.
- Below it are the actual instructions in ordinary Markdown, as numbered steps
- Invoke by describing the task in agent mode or addressing the skill directly with `/name`
- You do not need to write skills yourself: after completing a task with Copilot, ask it to make a skill from it (“Make a skill under `.agents/skills/` from what we just did”). Then read, shorten and test it.

**MCP**

- MCP (Model Context Protocol): an open standard through which the agent can use additional tools and data sources
- An MCP server is a small program that offers such tools to AI, e.g. searching documentation, accessing a ticket system or database. Configure which servers the agent may use in the editor. VS Code has a catalog in its extensions view.
- Security: every MCP server is code with access to your data; admins can block servers. Agent commands run with the editor's permissions, so read them before confirming.
- We demonstrate MCP without a separate exercise

#### 💪 05 Set up project rules and skills

AGENTS.md

```markdown
# grid_analysis

- Dependencies only via uv (`uv add`), never pip
- Tests: `uv run pytest`, Linting: `uv run ruff check`, Types: `uv run mypy src`
- domain.py: no file access, no print, no access to powerfactory
- Access PowerFactory only in data_source.py
- Descriptive names with units, no magic numbers
- NumPy-style docstrings; always specify units (pu, percent, kV)
- Always use pytest.approx for floating-point comparisons in tests
```

.agents/skills/check-solution/SKILL.md

```markdown
---
name: check-solution
description: Checks an exercise solution. Use when someone asks whether an exercise is complete or correct.
---

1. Run `uv run ruff check`, `uv run mypy src` and `uv run pytest`.
2. Read the task in `exercises/<number>/README.md` and check each criterion individually.
3. Report met / not met for each criterion with a brief explanation.
4. Do not reveal the solution. For unresolved points, only hint where to look.
```

**Part 1**

- Create the project rules for `grid_analysis` as `AGENTS.md` (template above) and add a rule of your own
- Ask Copilot Chat for a new function. Does it follow the rules?

**Part 2**

- Create the `check-solution` skill and have it check your solution to exercise 04
- Complete the task “Create an analysis that counts nodes with undervoltage” once with Copilot in agent mode, with a docstring (including units) and tests
- Ask Copilot to create the `new-analysis` skill from it. Read and shorten it.
- Test it in a new chat with “Create an analysis that counts nodes with overvoltage”

#### Summary

- Keep [AGENTS.md](http://AGENTS.md) as short as possible
- Not possible to generally improve the harness through [AGENTS.md](http://AGENTS.md) → The provider would have already done it if possible
- Use it to tell the agent how YOUR project works
- Use the skills in the next exercises where applicable

**More:** [Custom Instructions (Copilot)](https://docs.github.com/en/copilot/reference/custom-instructions-support) · [AGENTS.md](https://agents.md/) · [Agent Skills in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-agent-skills) · [MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers) · [MCP: introduction](https://modelcontextprotocol.io/docs/getting-started/intro) · [Rules Files for Safer Vibe Coding](https://www.wiz.io/blog/safer-vibe-coding-rules-files)

### Pure functions and inversion of control

**Why do this?** We write functions this way so we can test them without PowerFactory: quickly, without a license, using fixed data. What is easy to test is also easy to change and maintain.

- Side effect: anything a function does other than return a value, or reads from outside. Examples: reading or writing files, `print`, changing global variables or passed-in lists, fetching data from PowerFactory, checking the time.
- Pure function: same input, same output, no side effects. Can be tested without PowerFactory.
- Inversion of control: the function receives its data source instead of calling it directly
- In a test, a small fake object replaces the data source
- The current time, random numbers and files are also dependencies: `datetime.now()` inside a function makes it untestable. Better to pass the time as a parameter (`now: datetime`).
- In Python, a function parameter is usually enough. For larger dependencies, `typing.Protocol` describes the methods an object must have. Any class with those methods qualifies; it need not inherit from the protocol. Methods in the protocol have only `...` instead of a body.
- Target design “Functional Core, Imperative Shell”: the core contains domain logic as pure functions. The shell is the thin outer layer that fetches data, reads the time, writes files and calls the core.

```py
# Before: typical script, testable only with PowerFactory
def check_grid():
    app = powerfactory.GetApplication()
    app.GetFromStudyCase("ComLdf").Execute()
    violations = []
    for node in app.GetCalcRelevantObjects("*.ElmTerm"):
        u = node.GetAttribute("m:u")
        if u < 0.95 or u > 1.05:
            violations.append(node.loc_name)
    return violations

# After: domain logic receives the data
def voltage_band_violations(nodes: list[Node]) -> list[Node]:
    return [node for node in nodes if not within_voltage_band(node.voltage_pu)]
```

```py
from typing import Protocol

class DataSource(Protocol):
    def load_lines(self) -> list[Line]: ...

# The shell receives the data source
def check_lines(source: DataSource) -> list[Line]:
    return overloaded_lines(source.load_lines(), limit_percent=MAX_LOADING_PERCENT)

# In real use: reads from PowerFactory (in data_source.py)
class PowerFactoryDataSource:
    def __init__(self, app):
        self.app = app

    def load_lines(self) -> list[Line]:
        return [Line(l.loc_name, l.GetAttribute("c:loading"))
                for l in self.app.GetCalcRelevantObjects("*.ElmLne")]

# In tests: a fake providing fixed data
class FakeDataSource:
    def __init__(self, lines: list[Line]):
        self.lines = lines

    def load_lines(self) -> list[Line]:
        return self.lines

def test_check_lines():
    source = FakeDataSource([Line("L1", 80.0), Line("L2", 120.0)])
    assert [l.name for l in check_lines(source)] == ["L2"]
```

#### 💪 06 Separate domain logic from the data source

**Part 1 (without AI)**

- Open `exercises/06/grid_check.py`: a script in the style of a typical PowerFactory script. The function `create_check_report()` fetches data via the PowerFactory API, checks limits, reads the current time and writes a file.
- Mark all places with side effects
- Sketch on paper which parts should become pure and what should be passed in
- Assign each part to a module, **DON’T IMPLEMENT ANYTHING YET, WORK THROUGH IT CONCEPTUALLY/WITH PSEUDOCODE**: `domain.py` (core, only business logic and calculation, should be pure and testable!), `data_source.py` (PowerFactory access), `report.py` (build report string purely, write file). This is the module split from session 1, now with an explanation.

**Part 2 (with AI)**

- Ask Copilot Chat for its own proposed split and compare it with your sketch. Does the domain logic still access files, time or the data source?
- Ask Copilot to refactor according to your sketch
- Write a test using a fake data source returning three nodes, one with undervoltage
- Check the result with the `check-solution` skill

#### Summary

- Every split/abstraction has its cost! More lines to read and to maintain, more files to look at.
- Create tests where it really brings you value! If you feel uncertain about an implementation, try to create tests and if required, make it testable
- The bigger the thing to test is:
  - Tests will break more often and for various reasons
  - The quicker you are when writing the tests
- →  [https://www.esveo.com/en/blog/the-triangle-of-abstractions/](https://www.esveo.com/en/blog/the-triangle-of-abstractions/)

**More:** [Cosmic Python: abstractions](https://www.cosmicpython.com/book/chapter_03_abstractions.html) · [Cosmic Python: dependency injection](https://www.cosmicpython.com/book/chapter_13_dependency_injection.html) · [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)

### NumPy and performance

- NumPy is the foundation for almost all numerical work in Python. Its core is the array (`ndarray`): a table of numbers of the same type, with any number of dimensions, stored compactly in memory.
- SciPy builds on NumPy and provides ready-made scientific methods: linear algebra, optimization, integration, interpolation, signal processing, statistics and sparse matrices. `scipy.constants` also provides many physical constants otherwise typed into code by hand.
- Order: measure first, then vectorize, then parallelize
- Measure using standard-library tools: `time.perf_counter()` for simple measurements, `timeit` for short code snippets, `cProfile` to show which function consumes time
- Before optimizing, capture the current result in a test. This ensures the faster version computes the same result.
- Vectorization: replace a Python loop with an operation on the whole array

**Why is this faster?**

- In a Python loop, each number is a separate Python object. At each step the interpreter checks its type, finds the appropriate operation and creates a new object for the result. This overhead is much greater than the calculation itself.
- A NumPy array stores raw numbers tightly together, all of the same type. The type is checked once; then the loop runs in precompiled C code.
- The processor can also use its strengths: data is contiguous in fast cache memory and modern CPUs process several numbers in one instruction (SIMD)
- Result: typically 10–100 times faster

**Tools**

- Convention: `import numpy as np`, then use functions as `np.<name>`
- An array's `shape`: number of elements per dimension. A 2D array with 365 rows and 24 columns has shape `(365, 24)`.
- `axis` specifies the axis along which to aggregate: `.sum(axis=1)` gives one sum per row
- Boolean masks instead of `if` in loops: a comparison such as `values > 100` produces an array of `True`/`False`. Combine using `|` (or) and `&` (and); `True` counts as 1 when summed.
- Broadcasting: calculate with arrays of different shapes without loops. An array of shape `(1000, 5)` can be directly compared with one of shape `(5,)`; the smaller part is repeated for every row.
- Compare arrays in tests with `numpy.testing.assert_allclose(result, expected)`, the equivalent of `pytest.approx` for whole arrays
- SciPy: use ready-made solvers rather than writing your own. For network matrices, especially `scipy.sparse` for sparse matrices, whose entries are mostly zero.
- Parallelization of independent scenarios comes in the reserve session

```py
import time
import numpy as np

# Random temperatures: 365 days x 24 hours, mean 15, standard deviation 8
temperatures = np.random.default_rng(1).normal(15, 8, size=(365, 24))

start = time.perf_counter()
# Loop: count hot hours per day
hot_hours = [sum(1 for t in day if t > 25) for day in temperatures]
print(time.perf_counter() - start)

# Vectorized: mask + sum per row
hot_hours = (temperatures > 25).sum(axis=1)

# Broadcasting: separate limit per hour (shape (24,)) against (365, 24)
limit_per_hour = np.linspace(20, 30, 24)  # 24 evenly spaced values from 20 to 30
above_limit = (temperatures > limit_per_hour).sum(axis=1)
```

#### 💪 07 From loops to arrays

**Part 1 (without AI)**

- Open `exercises/07/scenarios.py`: nested loops count how many nodes violate the voltage band per scenario, for 1,000 scenarios × 5,000 nodes
- Measure the runtime
- Write a test that captures the current result (using `assert_allclose`)

**Part 2 (with AI)**

- Ask Copilot to propose a vectorized version and explain every NumPy operation
- Compare runtime and result (your test from part 1 must still pass)
- Extend it using broadcasting: each node gets its own limits (one array each of lower and upper limits per node, supplied by `powerfactory_fake`)

**More:** [NumPy: Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html) · [Why is NumPy fast?](https://numpy.org/doc/stable/user/whatisnumpy.html) · [SciPy Sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html) · [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html) · [Profiler](https://docs.python.org/3/library/profile.html)

### Planning, agent and review

- The quality of the result depends on the quality of the requirement
- First have a plan created and review it, then have it implemented
- Often you do not know all requirements in advance or think of every edge case. AI is good at uncovering such cases.
- Interview technique (“Grill me”): instead of implementing immediately, let AI interview you about the idea, one question at a time, until all details are clear. The result is the specification.
- Example prompt: “I want to build X. Ask me questions one at a time until the goal, inputs and outputs, edge cases and acceptance criteria are clear. Do not write code yet.” This can also be saved as a skill.
- Request a plan in the editor's plan mode or in agent mode with a clear instruction such as “Read the specification and create an implementation plan. Do not change any files yet.”
- Correct the plan in chat (“Skip step 3, write the tests first”) and only then approve implementation
- Agents are suitable for small, clearly bounded tasks with a goal, boundaries and tests as acceptance criteria
- Review every agent change as you would a colleague's work: read the diff, run tests, then accept
- A good specification includes the goal, inputs and outputs with units, edge cases, what must explicitly not happen, and how to verify the result

#### 💪 08 From specification to finished module

**Part 1 (without AI)**

- Task: a new module should summarize each line's loading across all scenarios (maximum, number of overloads, most critical scenario)
- Think about a specification; What do you want?

**Part 2 (with AI)**

- Ask Copilot to interview you about your specification (“Grill me”) and add edge cases you had not considered
- Ask Copilot to create a plan from it and correct the plan
- Have the agent implement it, including tests (the `new-analysis` skill should be triggered)
- Review the diff and check with `check-solution`
- Do a Code-review using a subagent to find mistakes
- Exchange specifications: what did AI misunderstand, and was it due to the specification?

**More:** [Grill me (AI Hero)](https://www.aihero.dev/skills-grill-me)

### API documentation (demo) and feedback

- Sphinx is the standard tool for Python documentation (Python's own documentation is created with it). It combines hand-written pages and docstrings from code into HTML, PDF and other formats.
- Extensions add functionality: `autodoc` reads docstrings from code; `napoleon` understands NumPy style
- NumPy style: a common docstring convention with fixed sections (Parameters, Returns, Raises, Examples)
- Needed in the code: type hints, purpose, parameters with units, return value, error cases and a short example
- Pitfall: `autodoc` imports modules to read docstrings. This fails without PowerFactory. Remedy: set `autodoc_mock_imports = ["powerfactory"]` so Sphinx replaces the module with an empty placeholder during the build.
- Local HTML is a folder of files that works directly in a browser without a server. Use the `singlehtml` builder for a single file (Sphinx calls its output formats builders).
- Two ways to create a PDF: `latexpdf`, which requires LaTeX (a typesetting system), or `rinohtype`, a Python package that generates PDFs without LaTeX
- Demo: build documentation for `grid_analysis`. Thanks to the project rules, the docstrings already use the right style.

**Feedback**

- What will you take away? What was missing?
- What should go into the reserve session?

**More:** [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) · [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html) · [NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html)

## Reserve session

Assembled as needed. Unfinished material from sessions 1 and 2 takes priority.

### Compiling to .pyd and .exe

- Python code is normally executed line by line at runtime by the interpreter (the `python` program). Here, compiling means translating the code in advance into machine code that the processor executes directly.
- `.pyd`: a compiled Python extension on Windows (technically a DLL, a Windows library) that can be imported like a normal module. It works only with the Python version with which it was built. This is why the `powerfactory` module also has a separate folder per Python version.
- `.exe`: an executable file containing the Python interpreter, your code and all dependencies. Runs on computers without a Python installation.

**The tools**

- C is an older compiled programming language. A C compiler translates C code into machine code. The following tools use it as an intermediate step.
- [Nuitka](https://nuitka.net/user-documentation/user-manual.html): translates Python code to C and compiles it. Can create both `.pyd` (`--module`) and `.exe` (`--standalone --onefile`). The code need not change.
- [Cython](https://cython.readthedocs.io/en/latest/src/quickstart/build.html): translates Python code to C, optionally with additional C type annotations for more speed. Creates `.pyd` and needs a little more setup. We use Nuitka in the exercise.
- [PyInstaller](https://pyinstaller.org/en/stable/usage.html): bundles the interpreter and code into an `.exe` without compiling. Simplest, but the code remains easy to extract.
- Nuitka and Cython need a C compiler: Visual Studio Build Tools on Windows
- Compiling makes extraction more difficult but does not prevent it
- Pitfalls: antivirus software often flags `.exe` files; the `.exe` must find the `powerfactory` module on the target computer
- Python loads a `.pyd` with the same name just like a `.py` file. If both are side by side, the `.pyd` takes precedence. Check with `print(module.__file__)`.

```powershell
uv add --dev nuitka pyinstaller

# .pyd from a module
uv run python -m nuitka --module src/grid_analysis/domain.py

# .exe with PyInstaller (result in dist/)
uv run pyinstaller --onefile src/grid_analysis/__main__.py

# .exe with Nuitka
uv run python -m nuitka --standalone --onefile src/grid_analysis/__main__.py
```

#### 💪 R1 A module as .pyd, the program as .exe

- Compile `domain.py` to a `.pyd` with Nuitka and check that importing it loads the `.pyd`
- Build an `.exe` from `__main__.py` with PyInstaller
- Copy the `.exe` from `dist/` to a folder outside the project and run it there in the terminal. It must run without `.venv`.

### Parallelization

- Independent calculations (e.g. scenarios) can be distributed across multiple CPU cores
- Process: an independently running program with its own memory. Thread: an execution stream within a process; multiple threads share memory.
- `ProcessPoolExecutor` (from the standard library's `concurrent.futures` module) starts multiple Python processes and distributes tasks among them
- `pool.map(function, values)` calls the function for each value, distributes the calls across processes and returns results in their original order
- Threads (`ThreadPoolExecutor`) hardly help with pure Python computation. Python has a lock, the GIL (Global Interpreter Lock), allowing only one thread to execute Python code at a time. Threads do help when waiting for files or the network.
- Processes have startup costs, and data must be copied between them. More processes than cores does not help.
- `if __name__ == "__main__":` encloses code that runs only when the file is started directly, not when imported. On Windows this is mandatory because each new process imports the file and would otherwise start more processes.

```py
from concurrent.futures import ProcessPoolExecutor

def compute(scenario: int) -> float:
    ...

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(compute, range(200)))
```

#### 💪 R2 Calculate scenarios in parallel

- Open `exercises/R2/simulation.py`: 200 independent scenario calculations run sequentially
- Parallelize them with `ProcessPoolExecutor`
- Measure with 1, 2, 4 and 8 processes (`max_workers`). At what point does it stop being worthwhile?
- What happens with `ThreadPoolExecutor`?

### API documentation exercise

Builds on the demo in session 2.

- Install: `uv add --dev sphinx`
- `uv run sphinx-quickstart docs` creates a documentation project with `docs/conf.py` (settings, in Python) and `docs/index.rst` (home page)
- `.rst` stands for reStructuredText, Sphinx's standard text format. Similar to Markdown, with slightly different syntax.
- Extensions are enabled in `docs/conf.py`; see the example
- `autosummary` automatically generates an overview page per module, so new modules appear without manual work
- Build: `uv run sphinx-build docs docs/_build/html`, then open `index.html` in a browser
- Write docstring examples (the `Examples` section) like an interactive Python session: lines beginning with `>>>` are input, followed by expected output. These examples are executable: `uv run pytest --doctest-modules src` checks that they are still correct.

```py
def within_voltage_band(voltage_pu: float) -> bool:
    """Checks whether a node voltage is within the voltage band.

    Examples
    --------
    >>> within_voltage_band(1.0)
    True
    >>> within_voltage_band(0.9)
    False
    """
```

```py
# docs/conf.py
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
autosummary_generate = True
autodoc_mock_imports = ["powerfactory"]
```

#### 💪 R3 Sphinx for your own project

- Install Sphinx, create a documentation project with `sphinx-quickstart` and enable `autodoc`, `napoleon` and `autosummary`
- Build HTML and open it locally in a browser
- Add an `Examples` section to two functions and check it with `uv run pytest --doctest-modules src`

### Git conflicts

- `git switch -c <name>`: create and switch to a new branch; `git switch main` switches back
- `git merge <name>`: merge changes from a branch into the current branch
- A conflict occurs when both branches have changed the same location. Git cannot decide which version is correct.
- Git marks the location in the file: between `<<<<<<<` and `=======` is the current branch's version; between `=======` and `>>>>>>>` is the version of the branch being merged
- Resolve: edit the file to the correct version, remove markers, `git add`, `git commit`. The editor offers a view with buttons for this.
- Always run tests after resolving
- `git log --oneline --graph`: shows history with branches

#### 💪 R4 Create and resolve a conflict

- Create two branches in the exercise repository, `limit-a` and `limit-b`
- Change the same line in `domain.py` differently on both branches (e.g. the lower voltage limit) and commit each
- Merge `limit-a`, then `limit-b` into `main` and resolve the conflict
- Run the tests and inspect the history with `git log --oneline --graph`

### Hands-on Snyk

- Snyk CLI is a separate program installed separately (see preparation). Connect it to the account once with `snyk auth` (opens the browser to sign in)
- `snyk test`: checks dependencies against a database of known vulnerabilities and identifies the version in which they were fixed
- `snyk code test`: checks your own code for insecure patterns
- uv project pitfall: Snyk can read `uv.lock` directly only in Early Access and on the Enterprise plan. A safer approach is to export dependencies to `requirements.txt`, the older, simple dependency-list format understood by almost all tools.
- `uv export --format requirements-txt > requirements.txt` (the `>` writes output to a file), then `snyk test --file=requirements.txt`
- Update a package: `uv lock --upgrade-package <package>` raises it to the latest permitted version in the lock file; `uv sync` installs it. If `pyproject.toml` disallows the new version, adjust its lower bound (`uv add "<package>>=<version>"`).

#### 💪 R5 Find a vulnerability

- Export dependencies and run `snyk test` and `snyk code test`
- A dependency has a known vulnerability: find it and update it with uv
- Then run the tests and check with `snyk test` that the finding has disappeared
