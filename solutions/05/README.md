# Solution 05: Set up project rules and skills

## Files

| File | Goes to |
| --- | --- |
| `AGENTS.md` | project folder |
| `.github/skills/check-solution/SKILL.md` | same path in the project |
| `.github/skills/new-analysis/SKILL.md` | same path in the project |
| `src/grid_analysis/domain.py` | with `count_undervoltage` and `count_overvoltage` |
| `tests/test_domain.py` | with the tests for both functions |

## Part 1: do the rules take effect?

The rule added to the template here is "One test per case, the test name describes the case". Yours will be different.

How to tell whether Copilot follows the rules: ask in a new chat for a function and check the answer against `AGENTS.md`. Does the name carry the unit? Is the docstring in NumPy style? Does it suggest `uv add` instead of `pip install`? If a rule is ignored again and again, it is usually worded too vaguely. "Good names" does nothing, "Descriptive names with units" does.

## Part 2: the skill `new-analysis`

The version Copilot generates from the finished task is usually three times as long and repeats what is already in `AGENTS.md`. Shortening means:

- remove everything the project rules already say
- keep the order of the steps, that is the actual value of the skill
- keep project-specific knowledge the AI cannot guess (which file, which constants)

The description decides whether the skill is loaded at all. It says when to use it: "Use when someone asks for a new check, count or calculation on nodes or lines."

The test in a new chat ("Add an analysis that counts nodes with overvoltage") shows whether the skill works: `count_overvoltage` should come out in the same shape as `count_undervoltage`, tests first, without you having to explain anything again.

## A detail worth discussing

`count_undervoltage` does not use `within_voltage_band`. A node with `NaN` as its voltage is not within the band, but it does not have undervoltage either. Both counting functions therefore ignore `NaN`: every comparison with `NaN` is `False`.
