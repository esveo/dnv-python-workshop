# Solution 03: Write your first tests yourself

## Part 1

The tests are in `tests/test_domain.py`. The test for the lower limit fails against the starting code:

```txt
    def test_lower_limit_belongs_to_band():
>       assert within_voltage_band(0.95)
E       assert False
```

The cause is in `domain.py`:

```py
return min_pu < voltage_pu <= max_pu  # bug: lower limit excluded
return min_pu <= voltage_pu <= max_pu  # fixed
```

The docstring says "the limits belong to the band", the code did something else at the lower limit. Neither Ruff nor mypy can find this: the code is valid, it is just wrong for the domain. Only a test that knows the expected behaviour catches it.

`NaN`: every comparison with `NaN` is `False`, so `within_voltage_band(float("nan"))` returns `False` without any special handling. The test pins this behaviour down so that nobody changes it by accident.

## Part 2 (TDD)

1. Red: write the tests for `is_overloaded` first. They fail with an `ImportError`, the function does not exist yet.
2. Green: the smallest implementation that makes them pass:

   ```py
   def is_overloaded(
       loading_percent: float, limit_percent: float = MAX_LOADING_PERCENT
   ) -> bool:
       return loading_percent >= limit_percent
   ```

3. Refactor: add the docstring, use the named constant instead of `100`.

Writing the test first forces the question "does exactly 100 % count as overloaded?" before any code exists.
