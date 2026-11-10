# grid_analysis

- Dependencies only via uv (`uv add`), never pip
- Tests: `uv run pytest`, linting: `uv run ruff check`, types: `uv run mypy src`
- domain.py: no file access, no print, no access to powerfactory
- Access to PowerFactory only in data_source.py
- Descriptive names with units, no magic numbers
- Docstrings in NumPy style, always state the units (pu, percent, kV)
- Floating point comparisons in tests always with pytest.approx
- One test per case, the test name describes the case
