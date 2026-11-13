# Solution 08: From specification to finished module

## Files

| File | Goes to |
| --- | --- |
| `docs/specs/loading.md` | same path in the project |
| `src/grid_analysis/loading_summary.py` | same path in the project |
| `tests/test_loading_summary.py` | same path in the project |

There is no single right solution here. Your specification decides what is right. This is one possible version.

## The specification

`docs/specs/loading.md` fits on one page. What makes it usable for an agent:

- units and shapes for every input and output, so nothing has to be guessed
- every edge case has a decision, not just a mention ("`NaN`: `ValueError`", not "handle `NaN`")
- the section "Must not happen" keeps the agent from adding sorting, output or its own limits
- the acceptance example is small enough to check by hand and contains the tie and the value on the limit

## Typical questions from the interview

The questions Copilot usually asks, and the answers this solution gives:

| Question | Decision |
| --- | --- |
| Is 100 % already overloaded? | Yes, as in `is_overloaded` |
| Two scenarios with the same maximum? | The first one in the given order |
| What about `NaN`? | `ValueError`. Ignoring would be possible (`np.nanmax`), but then the report has to say how many values were missing. |
| Return type? | List of frozen dataclasses. A dict by name would lose the order on duplicate names. |
| Should the result be sorted by loading? | No, the caller decides |
| No scenarios at all? | `ValueError` |

## The module

`summarise_loadings` checks the inputs first and then needs three NumPy operations along `axis=0` (one value per line): `max`, `argmax` and the sum over the mask `>= limit_percent`. `argmax` returns the first index of the maximum, which settles the tie exactly as specified.

Try it with the fake data:

```powershell
uv run python -c "from grid_analysis.loading_summary import summarise_loadings; from grid_analysis.powerfactory_fake import *; print(max(summarise_loadings(fake_loadings_percent(), fake_line_names(), fake_scenario_names()), key=lambda line: line.max_loading_percent))"
```

## Code review with a subagent

A prompt that works:

> Use a subagent to review the changes for the loading summary against docs/specs/loading.md. Report mistakes and missing edge cases, do not change any files.

The subagent starts with a fresh context: it does not know the chat in which the code was written and only judges what is in the files. Typical findings:

- an edge case from the specification without a test (e.g. names that do not match the shape)
- a test whose expected value was computed with the same formula as the module
- an error message that does not say which input is wrong

Check every finding yourself before you fix it. A subagent can be wrong as well.

## What to look for in the review

- Did the agent write the tests from the specification or from its own implementation? Tests that only repeat the code find nothing.
- Is the example from the specification among the tests, with exactly the expected values?
- Does the module import anything it must not (`powerfactory_fake`, `pathlib`)?
- Did it change files that were not part of the task?
- Where the result differs from what you wanted: was it in the specification?
