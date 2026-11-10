# 💪 07 From loops to arrays

**Topic:** NumPy and performance

`exercises/07/scenarios.py` counts, for 1,000 scenarios × 5,000 nodes, how many nodes per scenario violate the voltage band. It does so with nested Python loops. Order of work: measure first, then vectorise.

Try it:

```powershell
uv run python exercises/07/scenarios.py
```

## Part 1 (without AI)

1. Open `exercises/07/scenarios.py` and read `count_violations`
2. Measure the run time. The script already prints it. Run it several times: how much does the value vary?
3. Write a test in `exercises/07/test_scenarios.py` that pins down the current result (with `numpy.testing.assert_allclose`). Use small data so the test stays fast, e.g. `fake_voltages_pu(scenario_count=20, node_count=100)`, plus one tiny example you worked out by hand.

   ```powershell
   uv run pytest exercises/07
   ```

## Part 2 (with AI)

1. Let Copilot propose a vectorised version as a new function `count_violations_numpy` and let it explain every NumPy operation to you
2. Compare run time and result. Your test from part 1 has to stay green for the new function as well.
3. Extend it with broadcasting: every node gets its own limits. `fake_voltage_limits_pu()` from `powerfactory_fake` provides one array with a lower and one with an upper limit per node, each of shape `(5000,)`.

## Done when

- [ ] `exercises/07/test_scenarios.py` exists and pins down the result of the loop version with `assert_allclose`
- [ ] `count_violations_numpy` exists, contains no Python loop and returns the same result as the loop version
- [ ] There is a version with individual limits per node that uses broadcasting, with a test
- [ ] The script prints the run time of the loop version and of the NumPy version
- [ ] You can explain every NumPy operation in your solution (`shape`, mask, `|`, `axis`)
- [ ] `uv run pytest exercises/07` is green

## Hints

- Convention: `import numpy as np`
- `shape` of an array: number of elements per dimension. Here `(1000, 5000)`: one row per scenario, one column per node.
- Boolean masks instead of `if` in loops: a comparison like `values > 100` gives an array of `True`/`False`. Combine with `|` (or) and `&` (and), `True` counts as 1 when summing.
- `axis` states along which axis to aggregate: `.sum(axis=1)` gives one sum per row
- Broadcasting: an array of shape `(1000, 5000)` can be compared directly with one of shape `(5000,)`, the smaller one is repeated for every row
- Measuring: `time.perf_counter()` for simple measurements, `timeit` for short snippets, `cProfile` shows which function uses the time

## More

- [NumPy: Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Why is NumPy fast?](https://numpy.org/doc/stable/user/whatisnumpy.html)
- [SciPy Sparse](https://docs.scipy.org/doc/scipy/reference/sparse.html)
- [scipy.constants](https://docs.scipy.org/doc/scipy/reference/constants.html)
- [Profilers](https://docs.python.org/3/library/profile.html)
