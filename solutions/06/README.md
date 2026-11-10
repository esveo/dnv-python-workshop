# Solution 06: Separate domain logic from the data source

## Part 1: the side effects in `create_check_report()`

| Place in the script | Side effect |
| --- | --- |
| `powerfactory.GetApplication()`, `ActivateProject`, `ldf.Execute()` | reads from and changes PowerFactory |
| `app.GetCalcRelevantObjects(...)`, `GetAttribute(...)` | reads data from outside |
| `datetime.now()` | reads the clock: a different result on every call |
| `open("check_report.txt", "w")` | writes a file, to a fixed path |
| `app.PrintPlain(...)` | output |

What remains once all of that is removed is the actual domain logic: compare voltages with 0.95 and 1.05, compare loadings with 100, collect the violations. That part becomes pure.

## The split

| Module | Contents | Pure? |
| --- | --- | --- |
| `domain.py` | `CheckResult`, `check_grid(nodes, lines)` | yes |
| `report.py` | `format_check_report(result, now)` | yes, the time is passed in |
| `report.py` | `write_report(text, path)` | no, writes the file, the path is passed in |
| `data_source.py` | `DataSource` (protocol), `PowerFactoryDataSource` | no, access to PowerFactory |
| `grid_check.py` | `check(source)`, `create_check_report(source, now, path)`, `main()` | the shell: wires everything together |

The script moved from `exercises/06/grid_check.py` to `src/grid_analysis/grid_check.py`:

```powershell
uv run python -m grid_analysis.grid_check
```

`datetime.now()` and the fixed file name only appear in `main()`, at the very outside. Everything below it gets its dependencies passed in.

## The test

`tests/test_grid_check.py` contains a `FakeDataSource` with fixed nodes and lines. It does not inherit from `DataSource`: having the two methods is enough for the protocol. The tests need neither `powerfactory_fake` nor a licence, and they run in milliseconds.

Because the time is a parameter, the report text can be compared exactly. With `datetime.now()` inside, that would be impossible.

## What changed in content

Nothing. The limits are the same as in the script (below 0.95, above 1.05, from 100 %), they now come from the named constants in `domain.py`. One difference in the layout: the report lists all undervoltages first, then all overvoltages. The script listed the nodes in their original order.
