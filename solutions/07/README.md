# Solution 07: From loops to arrays

## Files

| File | Goes to |
| --- | --- |
| `exercises/07/scenarios.py` | same path in the project |

```powershell
uv run python exercises/07/scenarios.py
```

## Part 1: measure first

The loop version takes between a few tenths of a second and two seconds for 5 million values, depending on the machine. Between runs the value varies by a few percent, so one measurement is enough to see a factor of 30, but not to see a difference of 5 %.

The printed violations of the first five scenarios are the reference for the vectorised version. The script compares the full result of both versions with `np.array_equal` and prints `Same result: True`.

## Part 2: the vectorised version

```py
outside_band = (voltages_pu < MIN_VOLTAGE_PU) | (voltages_pu > MAX_VOLTAGE_PU)
return outside_band.sum(axis=1)
```

| Operation | What it does |
| --- | --- |
| `voltages_pu < MIN_VOLTAGE_PU` | compares every element, gives a boolean array of the same `shape` `(1000, 5000)`: a mask |
| `\|` | "or", element by element. The brackets are needed because `\|` binds more tightly than `<`. |
| `.sum(axis=1)` | `True` counts as 1. `axis=1` sums along the nodes, so one number per scenario remains: `shape` `(1000,)` |

The speed-up is around a factor of 30 to 100. The loop runs in compiled code inside NumPy, not in the Python interpreter.

## Things to check in an AI proposal

- Does it return an array or a list? Both are fine, but compare them with `np.array_equal`, not with `==`.
- `np.where(...)` or `np.count_nonzero(..., axis=1)` are equally valid. `.sum(axis=1)` on the mask is the shortest.
- A proposal with `for scenario in voltages_pu: np.sum(...)` is only half vectorised: one Python loop remains.
- `NaN` is never outside the band in this version, because every comparison with `NaN` is `False`. The loop version behaves the same way.
