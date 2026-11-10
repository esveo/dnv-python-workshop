# Specification: Loading summary per line

## Goal

Planners want to see at a glance which lines are critical across all calculated scenarios. The module condenses the loading of every line over all scenarios into three values. The result feeds a report, the module itself produces no output.

## Inputs

| Name | Type | Unit | Meaning |
| --- | --- | --- | --- |
| `loadings_percent` | NumPy array, shape `(scenarios, lines)` | percent | loading of every line in every scenario |
| `line_names` | list of `str`, one per column | | names of the lines |
| `scenario_names` | list of `str`, one per row | | names of the scenarios |
| `limit_percent` | `float`, default `MAX_LOADING_PERCENT` (100.0) | percent | loading limit |

## Outputs

A list with one `LineSummary` per line, in the order of `line_names`:

| Field | Type | Unit | Meaning |
| --- | --- | --- | --- |
| `name` | `str` | | name of the line |
| `max_loading_percent` | `float` | percent | highest loading over all scenarios |
| `overload_count` | `int` | scenarios | number of scenarios in which the line is overloaded |
| `most_critical_scenario` | `str` | | name of the scenario with the highest loading |

## Edge cases

- A loading exactly on the limit counts as overloaded (`>=`), as in `is_overloaded`
- Several scenarios with the same maximum: the first one in the order of `scenario_names` wins
- A line that is never overloaded still appears, with `overload_count` 0
- A missing value (`NaN`) anywhere in the data: `ValueError`. A summary that silently skips values would look more reliable than it is.
- `line_names` or `scenario_names` do not match the shape of the data: `ValueError` that names both numbers
- No scenarios (zero rows): `ValueError`, there is no maximum
- No lines (zero columns): empty list
- The data is not two-dimensional: `ValueError`

## Must not happen

- No access to `powerfactory` or `powerfactory_fake`, no file, no `print`
- The input array is not modified
- No sorting or filtering of the lines: that is the caller's decision
- No new limit constants: the default comes from `domain.py`

## Acceptance

`uv run ruff check`, `uv run mypy src` and `uv run pytest` are green. The tests contain this example:

| | L1 | L2 | L3 |
| --- | --- | --- | --- |
| Base | 80.0 | 100.0 | 50.0 |
| Peak | 120.0 | 90.0 | 50.0 |
| Outage | 120.0 | 110.0 | 40.0 |

Expected:

| Line | Max. loading | Overloads | Most critical scenario |
| --- | --- | --- | --- |
| L1 | 120.0 | 2 | Peak (first of two equal maxima) |
| L2 | 110.0 | 2 (100.0 counts) | Outage |
| L3 | 50.0 | 0 | Base |
