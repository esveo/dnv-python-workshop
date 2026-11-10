# Solution 02: Fix the findings

Add to `pyproject.toml`:

```toml
[tool.ruff.lint]
extend-select = ["B", "I", "N"]
```

The fixed files are in `src/grid_analysis/`.

## The findings: bug or style?

| Finding | Where | Bug or style? |
| --- | --- | --- |
| `I001` unsorted imports | `domain.py`, `report.py` | Style. `ruff check --fix` sorts them. |
| `F401` unused import `os` | `report.py` | Style. Dead code that misleads readers. |
| `F541` f-string without placeholders | `report.py` | Style. |
| `F841` unused variable `total` | `report.py` | Style here. Often a hint at a forgotten calculation, so always worth a look. |
| `N802`, `N803` `formatLine(Name, ...)` | `report.py` | Style (PEP 8 naming). |
| `N806` variable `Result` | `data_source.py` | Style. |
| `E722` bare `except` | `domain.py` | Real risk. It swallows every error, including typos, and returns 0 instead. The fix handles the one expected case, the empty list, explicitly. |
| `B006` mutable default `names=[]` | `domain.py` | Real bug. The list is created once and shared by all calls: from the second call on, the names of earlier calls are still in it. |
| mypy `Missing return statement` | `domain.py`, `find_node` | Real bug. The function returns `None` when nothing is found, but promises a `Node`. The caller crashes later, somewhere else. The fix makes it honest: `-> Node | None`. |
| mypy `Incompatible return value type` | `report.py`, `share_percent` | Wrong promise. The division returns a `float`, the type hint said `int`. |

Depending on the Ruff version, some of these findings already show up before you enable `B`, `I` and `N`: newer versions enable more rules by default.

## The function `p`

`p(u, i, x)` computes the active power in a three-phase system: P = √3 · U · I · cos φ. `1.732` is √3, the division by 1000 converts W to kW. No tool reports this function, yet it is the hardest one to read in the whole file.

```py
SQRT_3 = math.sqrt(3)
WATTS_PER_KILOWATT = 1000


def three_phase_active_power_kw(
    voltage_v: float, current_a: float, power_factor: float
) -> float:
    """Active power in a three-phase system in kW: P = √3 · U · I · cos φ."""
    return SQRT_3 * voltage_v * current_a * power_factor / WATTS_PER_KILOWATT
```

The bug at the lower limit of `within_voltage_band` is still in there. No static tool finds it. That is what the tests in exercise 03 are for.
