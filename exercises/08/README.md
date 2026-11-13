# 💪 08 From specification to finished module

**Topic:** Planning, agent, review

The quality of the result depends on the quality of the requirement. You write a specification, let the AI interview you about it, have it draw up a plan, and only then let the agent implement.

## The task

A new module summarises the loading of every line across all scenarios:

- the maximum loading
- the number of overloads
- the most critical scenario

Data is provided by `powerfactory_fake`:

```py
from grid_analysis.powerfactory_fake import (
    fake_line_names,  # 50 names, matching the columns
    fake_loadings_percent,  # array of shape (200, 50): scenarios x lines, in percent
    fake_scenario_names,  # 200 names, matching the rows
)
```

## Part 1 (without AI)

1. Think about the specification: what exactly do you want? Write it yourself in `docs/specs/loading.md`, one page at most. A template is in [spec-template.md](spec-template.md).

## Part 2 (with AI)

1. Let Copilot interview you about your specification ("grill me") and add the edge cases you did not think of:

   > I want to build the module described in docs/specs/loading.md. Ask me questions one at a time until goal, inputs and outputs, edge cases and acceptance are clear. Do not write any code yet.

2. Let Copilot draw up a plan from it (in plan mode, or in agent mode with a clear instruction) and correct it in the chat:

   > Read the specification and create an implementation plan. Do not change any files yet.

3. Let the agent implement it, including tests. The skill `new-analysis` should kick in.
4. Review the diff and check with `check-solution`
5. Do a code review using a subagent to find mistakes, e.g.:

   > Use a subagent to review the changes for this module against docs/specs/loading.md. Report mistakes and missing edge cases, do not change any files.

6. Swap specifications with your neighbour: what did the AI misunderstand, and was the specification the reason?

## Done when

- [ ] `docs/specs/loading.md` exists, is one page at most and covers: goal, inputs and outputs with units, edge cases, what must explicitly not happen, how to verify the result
- [ ] The specification states what happens with: a loading exactly on the limit, several scenarios with the same maximum, missing values (`NaN`), names that do not match the shape of the data
- [ ] A new module under `src/grid_analysis/` provides, per line, the maximum loading, the number of overloads and the most critical scenario
- [ ] The module is pure: no access to `powerfactory`, no file, no `print`
- [ ] There are tests with small data worked out by hand, including the edge cases from the specification
- [ ] `check-solution` and a subagent code review ran, and you dealt with their findings
- [ ] `uv run ruff check`, `uv run mypy src` and `uv run pytest` are green

## Hints

- Often you do not know all requirements in advance or think of every edge case. AI is good at uncovering such cases: let it interview you ("grill me") before it writes code. You can also save this interview prompt as a skill.
- A good specification: goal, inputs and outputs with units, edge cases, what must explicitly not happen, how to verify the result
- Agents suit small, clearly bounded tasks with a goal, limits and tests as acceptance
- Every change by the agent gets checked like a colleague's work: read the diff, run the tests, then accept
- A subagent starts with a fresh context and only sees what it is given. That makes it a more independent reviewer than the chat that wrote the code.
- You correct the plan in the chat ("drop step 3, write the tests first") and only then approve the implementation

## More

- [Grill me (AI Hero)](https://www.aihero.dev/skills-grill-me)
