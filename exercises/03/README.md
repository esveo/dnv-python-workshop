# 💪 03 Write your first tests yourself (without AI)

**Topic:** Unit tests

You write the first tests entirely yourself, without Copilot. Best switch autocomplete off for this exercise.

## Part 1

1. Open `src/grid_analysis/domain.py` and `tests/test_domain.py`
2. Write tests for `within_voltage_band(voltage_pu: float) -> bool`:
   - within the band
   - outside, below and above
   - exactly on the limits (0.95 and 1.05 p.u., both belong to the band)
   - `NaN` (a missing measurement is not within the band)
3. Run the tests: `uv run pytest`
4. One of your tests fails because the implementation has a bug at a limit. Find and fix it.

## Part 2 (TDD)

1. First write tests for a new function that does not exist yet:

   ```py
   def is_overloaded(loading_percent: float, limit_percent: float = 100) -> bool:
   ```

   The limit itself counts as overloaded: 100 % with a limit of 100 gives `True`.

2. Let the tests fail (red)
3. Implement the function in `domain.py` until all tests are green (green)
4. Tidy up, the tests stay green (refactor)

## Done when

- [ ] `tests/test_domain.py` contains tests for `within_voltage_band`: within, below, above, both limits, `NaN`
- [ ] The bug at the lower limit of `within_voltage_band` is fixed
- [ ] `is_overloaded` exists in `domain.py`, with type hints and a docstring
- [ ] There are tests for `is_overloaded`: below, above, exactly on the limit, custom limit
- [ ] Every test checks exactly one case and has a name that describes the case
- [ ] `uv run pytest` is green

## Hints

- Structure of a test: arrange (prepare the inputs), act (call the function), assert (check the result)
- pytest finds tests in files named `test_*.py` and functions named `test_*`
- Create `NaN` with `float("nan")`. Every comparison with `NaN` is `False`, even `NaN == NaN`.
- Never compare floating point numbers with `==`, use a tolerance: `assert result == pytest.approx(0.3)`
- Run a single test: `uv run pytest -k limit`

## More

- [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Test-Driven Development (Martin Fowler)](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
