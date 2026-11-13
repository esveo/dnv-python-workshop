# grid_analysis

- Dependencies only via uv (`uv add`), never pip
- Tests: `uv run pytest`, Linting: `uv run ruff check`, Types: `uv run mypy src`
- domain.py: no file access, no print, no access to powerfactory
- Access PowerFactory only in data_source.py
- Descriptive names with units, no magic numbers
- NumPy-style docstrings; always specify units (pu, percent, kV)
- Always use pytest.approx for floating-point comparisons in tests
- One test per case, the test name describes the case
