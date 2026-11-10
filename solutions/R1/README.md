# Solution R1: A module as .pyd, the program as .exe

There are no files for this exercise, only commands. Everything runs in the project folder on Windows.

## 1. Compile `domain.py` into a `.pyd`

```powershell
uv run python -m nuitka --module src/grid_analysis/domain.py --output-dir=src/grid_analysis
```

Nuitka translates the module to C and calls the C compiler. On the first run it asks whether it may download additional tools: answer `yes`. Afterwards the folder contains:

```txt
src/grid_analysis/domain.py
src/grid_analysis/domain.cp312-win_amd64.pyd
src/grid_analysis/domain.pyi
src/grid_analysis/domain.build/
```

`cp312` in the file name is the Python version, `win_amd64` the platform. With another Python version the file is simply not found.

## 2. Check the import

```powershell
uv run python -c "import grid_analysis.domain as m; print(m.__file__)"
```

The path ends in `.pyd`. The `.py` file is still there, but the `.pyd` wins. `uv run pytest` stays green: the tests cannot tell the difference.

## 3. Build the `.exe` with PyInstaller

```powershell
uv run pyinstaller --onefile --name grid_analysis src/grid_analysis/__main__.py
```

Result: `dist/grid_analysis.exe`, plus the folder `build/` and the file `grid_analysis.spec`.

## 4. Start it outside the project

```powershell
Copy-Item dist\grid_analysis.exe $env:TEMP
cd $env:TEMP
.\grid_analysis.exe
```

The report appears, without `uv` and without `.venv`. The first start takes a moment: a one-file `.exe` unpacks itself into a temporary folder first.

## 5. Optional: Nuitka instead of PyInstaller

```powershell
uv run python -m nuitka --standalone --onefile src/grid_analysis/__main__.py
```

| | PyInstaller | Nuitka |
| --- | --- | --- |
| Build time | seconds | minutes |
| What ends up in the `.exe` | interpreter plus bytecode | interpreter plus compiled C code |
| Reading the code out | easy | hard, but not impossible |

Both files contain NumPy and SciPy as soon as the program imports them. That is what makes them large, not your own code.

## 6. Clean up

```powershell
Remove-Item src\grid_analysis\domain.*.pyd, src\grid_analysis\domain.pyi
Remove-Item -Recurse src\grid_analysis\domain.build, build, dist
Remove-Item grid_analysis.spec
```

`git status` should not have shown any of these files before either: `.gitignore` covers `*.pyd`, `*.pyi`, `*.build/`, `build/`, `dist/` and `*.spec`.

## Why a `.pyd` is tied to the Python version

A `.pyd` is a Windows DLL that calls functions of the Python interpreter directly. Those internal interfaces change between versions such as 3.12 and 3.13. PowerFactory ships its `powerfactory.pyd` for the same reason in one folder per Python version.
