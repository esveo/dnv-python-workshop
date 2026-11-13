# 💪 05 Set up project rules and skills

**Topic:** Project rules, skills and MCP

Without rules, the AI guesses your conventions anew in every session. You create project rules and two skills that apply to all exercises from now on.

## Part 1

1. Create the project rules as `AGENTS.md` in the project folder. Template:

   ```markdown
   # grid_analysis

   - Dependencies only via uv (`uv add`), never pip
   - Tests: `uv run pytest`, Linting: `uv run ruff check`, Types: `uv run mypy src`
   - domain.py: no file access, no print, no access to powerfactory
   - Access PowerFactory only in data_source.py
   - Descriptive names with units, no magic numbers
   - NumPy-style docstrings; always specify units (pu, percent, kV)
   - Always use pytest.approx for floating-point comparisons in tests
   ```

2. Add a rule of your own
3. In a new chat, ask Copilot for a new function, e.g. "Write a function that returns the highest loading of all lines". Does it follow the rules?

## Part 2

1. Create the skill `check-solution` as the file `.agents/skills/check-solution/SKILL.md`:

   ```markdown
   ---
   name: check-solution
   description: Checks an exercise solution. Use when someone asks whether an exercise is complete or correct.
   ---

   1. Run `uv run ruff check`, `uv run mypy src` and `uv run pytest`.
   2. Read the task in `exercises/<number>/README.md` and check each criterion individually.
   3. Report met / not met for each criterion with a brief explanation.
   4. Do not reveal the solution. For unresolved points, only hint where to look.
   ```

2. Let it check your solution of exercise 04 in agent mode: "Is exercise 04 done?" or directly `/check-solution 04`
3. Do the following task once with Copilot in agent mode: "Add an analysis that counts nodes with undervoltage", with a docstring (including units) and tests
4. Let Copilot turn that into the skill `new-analysis`: "Make a skill under `.agents/skills/` from what we just did". Read it and shorten it.
5. Test it in a new chat with "Add an analysis that counts nodes with overvoltage"

From here on, use both skills in the exercises wherever they fit.

## Done when

- [ ] `AGENTS.md` is in the project folder and contains the rules of the template plus at least one of your own
- [ ] `.agents/skills/check-solution/SKILL.md` exists, with `name` and `description` in the header
- [ ] `.agents/skills/new-analysis/SKILL.md` exists, with `name` and `description` in the header and numbered steps
- [ ] `domain.py` contains one function each that counts nodes with undervoltage and with overvoltage, both with a NumPy style docstring and units
- [ ] Both functions have tests, including the limits of the voltage band
- [ ] `uv run ruff check`, `uv run mypy src` and `uv run pytest` are green

## Hints

- Copilot attaches the project rules to every request. So keep `AGENTS.md` as short as possible: every line costs space on every request.
- Use the rules to tell the agent how *your* project works. They cannot generally make the AI better: if that were possible, the provider would already have done it.
- Every skill is a folder under `.agents/skills/` with a `SKILL.md`. Invoke it by describing the task in agent mode or directly with `/name`.
- At first the AI only sees the description of a skill. It should therefore say when the skill is to be used.
- Skills and MCP only work in agent mode
- New task, new chat: a new chat starts empty and shows whether rules and skills really take effect
- `AGENTS.md` is an open standard that Copilot and many other AI tools read. The alternative `.github/copilot-instructions.md` only works with Copilot.

Docstring in NumPy style:

```py
def overloaded_lines(lines: list[Line], limit_percent: float) -> list[Line]:
    """Return all lines whose loading reaches or exceeds the limit.

    Parameters
    ----------
    lines
        Lines to check.
    limit_percent
        Loading limit in percent, e.g. 100.

    Returns
    -------
    list[Line]
        The overloaded lines in their original order.
    """
```

## More

- [Custom Instructions (Copilot)](https://docs.github.com/en/copilot/reference/custom-instructions-support)
- [AGENTS.md](https://agents.md/)
- [Agent Skills in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-agent-skills)
- [MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [MCP: Introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Rules Files for Safer Vibe Coding](https://www.wiz.io/blog/safer-vibe-coding-rules-files)
