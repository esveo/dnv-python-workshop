# Solution 04: AI writes tests, you review them

The tests for `overloaded_lines` are at the end of `tests/test_domain.py`. Your tests from Copilot will look different. What matters is the review.

## What to look for in the review

**Does the test rebuild the implementation?** A typical AI test:

```py
def test_overloaded_lines():
    lines = [Line("L1", 80.0), Line("L2", 120.0)]
    expected = [line for line in lines if line.loading_percent >= 100.0]
    assert overloaded_lines(lines, 100.0) == expected
```

It contains the same expression as the function. If the function is wrong, the test is wrong in the same way and stays green. Better: write the expectation down by hand, `[Line("L2", 120.0)]`.

**Is the limit covered?** AI tests like to use comfortable values such as 80 and 120. Then `>` and `>=` behave the same. Only a line with exactly 100.0 tells them apart.

**Is there one case per test, with a name that describes it?** One big test with ten asserts fails at the first one and hides the rest.

## Part 2: the deliberate bug

With `>` instead of `>=` in `overloaded_lines`:

```txt
FAILED tests/test_domain.py::test_line_exactly_on_the_limit_counts_as_overloaded
```

Exactly one test fails, the one for the limit. Without it, the bug would go unnoticed.

## Coverage

```powershell
uv run pytest --cov=grid_analysis --cov-report=term-missing
```

The report shows `report.py` and `__main__.py` as largely untested, and in `domain.py` the functions without tests (`mean_voltage_pu`, `find_node`, `collect_names`, `three_phase_active_power_kw`). Coverage only tells you which lines ran, not whether the result was checked: the limit bug from exercise 03 sat in a line with 100 % coverage.
