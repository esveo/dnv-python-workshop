# 💪 06 Separate domain logic from the data source

**Topic:** Pure functions and inversion of control

`exercises/06/grid_check.py` is a script in the style of a typical PowerFactory script. The function `create_check_report()` fetches data through the PowerFactory API, checks limits, reads the current time and writes a file. It cannot be tested like this. We change that.

Try it:

```powershell
uv run python exercises/06/grid_check.py
```

The script writes `check_report.txt` into the current folder.

## Part 1 (without AI)

1. Open `exercises/06/grid_check.py`
2. Mark every place with a side effect (as a comment or on paper): what does the function read from outside, what does it cause apart from its return value?
3. Sketch on paper which parts should become pure and what gets passed in
4. Assign every part to a module:
   - `domain.py` (core): only domain logic and calculations, e.g. checking the limits. Pure and testable.
   - `data_source.py`: access to PowerFactory
   - `report.py`: building the report text (pure), writing the file

   This is the module split from session 1, now with a reason.

**Do not implement anything yet.** Work through it conceptually, on paper or in pseudocode. The code changes happen in part 2.

## Part 2 (with AI)

1. Let Copilot make its own proposal for the split in the chat and compare it with your sketch. Does the domain logic part still access files, the time or the data source?
2. Let Copilot carry out the refactoring according to your sketch. The code moves from `exercises/06/grid_check.py` to `src/grid_analysis/`.
3. Write a test with a fake data source that provides three nodes, one of them with undervoltage
4. Check the result with the skill `check-solution`

## Done when

- [ ] The limit checks are a pure function in `domain.py`: no access to `powerfactory`, no file, no `print`, no `datetime.now()`
- [ ] Access to PowerFactory lives in `data_source.py`, behind a data source that gets passed in (e.g. a `typing.Protocol` with `load_nodes` and `load_lines`)
- [ ] The time of the report is passed as a parameter (`now: datetime`), `datetime.now()` only remains at the very outside
- [ ] Writing the file lives in `report.py`, the path is passed in
- [ ] There is a test with a fake data source with three nodes, one of them with undervoltage. The test needs neither `powerfactory_fake` nor a file.
- [ ] The report has the same content as before
- [ ] `uv run ruff check`, `uv run mypy src` and `uv run pytest` are green

## Hints

- Side effect: everything a function causes apart from its return value, or reads from outside. The time and random numbers count too.
- Functional core, imperative shell: the core holds the domain logic as pure functions. The shell is the thin outer part that fetches data, reads the time, writes files and then calls the core.
- A `Protocol` describes which methods an object must have. Any class with these methods fits, it does not have to inherit from it:

  ```py
  from typing import Protocol


  class DataSource(Protocol):
      def load_lines(self) -> list[Line]: ...


  class FakeDataSource:
      def __init__(self, lines: list[Line]):
          self.lines = lines

      def load_lines(self) -> list[Line]:
          return self.lines
  ```

- Files in tests: with the parameter `tmp_path`, pytest provides an empty temporary folder
- Every split and every abstraction has its cost: more lines to read and maintain, more files to look at. Split where it brings value.
- Write tests where they really help you. If you feel unsure about an implementation, write tests for it and, if necessary, make it testable first.
- The bigger the unit under test, the faster the tests are written, but the more often and for more reasons they break

## More

- [Cosmic Python: Abstractions](https://www.cosmicpython.com/book/chapter_03_abstractions.html)
- [Cosmic Python: Dependency Injection](https://www.cosmicpython.com/book/chapter_13_dependency_injection.html)
- [Functional Core, Imperative Shell](https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell)
- [The Triangle of Abstractions](https://www.esveo.com/en/blog/the-triangle-of-abstractions/)
