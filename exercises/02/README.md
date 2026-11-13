# 💪 02 Fix findings

**Topic:** Code quality and static analysis

The starting code in `src/grid_analysis/` contains style problems and a few real bugs on purpose. Ruff and mypy find most of them.

## Part 1 (without AI)

1. Run `uv run ruff check` and `uv run mypy src` in the exercise repository
2. Additionally enable the Ruff rule sets `B`, `I` and `N` in `pyproject.toml`:

   ```toml
   [tool.ruff.lint]
   extend-select = ["B", "I", "N"]
   ```

   The section `[tool.ruff.lint.per-file-ignores]` already exists, leave it in place.

3. Run `uv run ruff check` again. What is new?
4. Fix the first three findings yourself. Every finding has a code (e.g. `B006`) under which the [Ruff docs](https://docs.astral.sh/ruff/rules/) explain why the rule exists.
5. Install the Ruff extension (`charliermarsh.ruff`, VS Code recommends it for this repository) and turn on format on save:
   1. In a Python file, open the command palette with Ctrl+Shift+P
   2. Search for "Format Document With" and select "Configure Default Formatter"
   3. Select Ruff
   4. Open the settings by searching "Open Settings (UI)" in the command palette
   5. Turn on "Format On Save"
   6. Edit a file and save it to format it

## Part 2 (with AI)

1. For two more findings, let Copilot explain why the rule exists and let it fix them
2. Fix the rest until `uv run ruff check` and `uv run mypy src` report nothing
3. Which findings were real bugs, which were only style?
4. `domain.py` contains a function with single-letter names and magic numbers. No tool reports it. Rename it together with Copilot: what does it calculate, which units do the parameters have, what does `1.732` mean?

## Done when

- [ ] `uv run ruff check` reports no errors, with the rule sets `B`, `I` and `N` enabled
- [ ] `uv run mypy src` reports no errors
- [ ] `uv run python -m grid_analysis` still prints the report, `uv run pytest` is green
- [ ] The function `p` in `domain.py` has a descriptive name, parameters with the unit in the name, type hints, a docstring and no magic number
- [ ] The Ruff extension is installed, set as the default formatter, and saving a Python file formats it
- [ ] For every finding you fixed, you can say whether it was a real bug or only style

## Hints

- `uv run ruff check --fix` repairs simple cases automatically. Look at what would change first: `uv run ruff check --diff`
- `uv run ruff format` brings the code into a uniform shape
- The fake module deliberately uses the spelling of the real PowerFactory API (`GetApplication`). That is why the naming rule is switched off there.
- Do not type natural constants yourself: `math.sqrt(3)`, `math.pi` or `scipy.constants`

## More

- [PEP 8](https://peps.python.org/pep-0008/)
- [Code Smells](https://refactoring.guru/refactoring/smells)
- [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html)
- [Snyk: uv support](https://docs.snyk.io/supported-languages/supported-languages-list/python/cli-support-for-uv)
