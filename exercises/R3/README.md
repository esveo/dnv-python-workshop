# 💪 R3 Sphinx for your own project

**Topic:** API documentation

You generate HTML documentation for `grid_analysis` from the docstrings in the code. Sphinx is already in the project.

## Task

1. Create a documentation project:

   ```powershell
   uv run sphinx-quickstart docs
   ```

   Answer "Separate source and build directories" with `n`. The result is `docs/conf.py` (settings, in Python) and `docs/index.rst` (start page).

2. Enable `autodoc`, `napoleon` and `autosummary` in `docs/conf.py`:

   ```py
   extensions = [
       "sphinx.ext.autodoc",
       "sphinx.ext.napoleon",
       "sphinx.ext.autosummary",
   ]
   autosummary_generate = True
   autodoc_mock_imports = ["powerfactory"]
   ```

3. Add an overview of the modules to `docs/index.rst`:

   ```rst
   .. autosummary::
      :toctree: _autosummary
      :recursive:

      grid_analysis
   ```

   The overview lists every function with the first line of its docstring. For the full docstrings of one module, add below it:

   ```rst
   Domain logic
   ------------

   .. automodule:: grid_analysis.domain
      :members:
      :no-index:
   ```

4. Build the HTML and open `docs/_build/html/index.html` in the browser:

   ```powershell
   uv run sphinx-build docs docs/_build/html
   ```

5. Add an `Examples` section to two functions and check it:

   ```powershell
   uv run pytest --doctest-modules src
   ```

## Done when

- [ ] `docs/conf.py` enables `autodoc`, `napoleon` and `autosummary`
- [ ] `uv run sphinx-build docs docs/_build/html` runs without errors
- [ ] The HTML shows the functions from `domain.py` with their docstrings, opened locally in the browser without a server
- [ ] Two functions have an `Examples` section, and `uv run pytest --doctest-modules src` is green
- [ ] `docs/_build/` does not show up in `git status`

## Hints

- `.rst` stands for reStructuredText, the standard text format of Sphinx. Similar to Markdown, with slightly different syntax. Indentation matters.
- `autodoc` imports the modules to read the docstrings. Without PowerFactory that fails for the real module. `autodoc_mock_imports = ["powerfactory"]` replaces the module with an empty placeholder during the build.
- Examples in docstrings look like an interactive Python session: lines with `>>>` are the input, the expected output is below.

  ```py
  def within_voltage_band(voltage_pu: float) -> bool:
      """Check whether a node voltage lies within the voltage band.

      Examples
      --------
      >>> within_voltage_band(1.0)
      True
      >>> within_voltage_band(0.9)
      False
      """
  ```

- As a single file: `uv run sphinx-build -b singlehtml docs docs/_build/singlehtml`
- PDF either via `latexpdf` (needs a LaTeX installation) or via `rinohtype` (a Python package that creates PDFs without LaTeX)

## More

- [autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
- [napoleon](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [autosummary](https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html)
- [NumPy docstring style](https://numpydoc.readthedocs.io/en/latest/format.html)
