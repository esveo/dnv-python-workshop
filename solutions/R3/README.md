# Solution R3: Sphinx for your own project

## Files

| File | Goes to |
| --- | --- |
| `docs/conf.py` | same path in the project |
| `docs/index.rst` | same path in the project |
| `src/grid_analysis/domain.py` | with `Examples` in `within_voltage_band` and `is_overloaded` |

`sphinx-quickstart` also creates `docs/Makefile`, `docs/make.bat` and the empty folders `_static` and `_templates`. They are not needed for the commands below and are left out here.

```powershell
uv run sphinx-build docs docs/_build/html
uv run pytest --doctest-modules src
```

Then open `docs/_build/html/index.html` with a double click.

## `conf.py`

Besides the three extensions from the task there is one more change: `exclude_patterns` contains `specs`. Otherwise Sphinx warns about `docs/specs/loading.md` from exercise 08, a file it does not know what to do with.

The project is installed in the `.venv` by `uv sync`, so `autodoc` can import `grid_analysis` directly. In projects without that, `conf.py` needs a `sys.path.insert(0, ...)` pointing to `src`.

## `index.rst`

```rst
.. autosummary::
   :toctree: _autosummary
   :recursive:

   grid_analysis
```

`:recursive:` walks through the package and creates one page per module in `docs/_autosummary/`. Those pages are generated on every build, which is why the folder is in `.gitignore`.

The generated module pages only list each function with the first line of its docstring. The full docstrings come from the second directive:

```rst
.. automodule:: grid_analysis.domain
   :members:
   :no-index:
```

`:members:` includes every function and class of the module. `:no-index:` avoids a warning: the module is already registered once by its `autosummary` page.

Indentation matters in `.rst`: the options and the module name are indented by three spaces, with an empty line between them.

## What the HTML shows

- NumPy-style docstrings (from exercise 05) appear as formatted lists with "Parameters" and "Returns". That is the work of `napoleon`.
- Functions without a docstring appear with their signature only
- `powerfactory_fake` appears as well, with its methods in PowerFactory spelling

## Docstring examples

```py
def is_overloaded(
    loading_percent: float, limit_percent: float = MAX_LOADING_PERCENT
) -> bool:
    """Check whether a loading reaches or exceeds the limit.

    Examples
    --------
    >>> is_overloaded(104.2)
    True
    >>> is_overloaded(100.0)
    True
    """
```

`uv run pytest --doctest-modules src` runs every `>>>` line and compares the output character by character. That way an example in the documentation cannot go stale unnoticed.

Careful with floating point output: `>>> 0.1 + 0.2` gives `0.30000000000000004`. Examples with `True`/`False`, whole numbers or rounded values are robust.

## Other formats

```powershell
uv run sphinx-build -b singlehtml docs docs/_build/singlehtml
```

One HTML file instead of many, handy for passing on.
