# 💪 R1 A module as .pyd, the program as .exe

**Topic:** Compiling to `.pyd` and `.exe`

You compile a single module into a `.pyd` and bundle the whole program into an `.exe`.

Prerequisite: Windows with the Visual Studio Build Tools (C compiler for Nuitka). Nuitka and PyInstaller are already in the project.

## Task

1. Compile `domain.py` into a `.pyd` with Nuitka:

   ```powershell
   uv run python -m nuitka --module src/grid_analysis/domain.py --output-dir=src/grid_analysis
   ```

2. Check that the import loads the `.pyd`:

   ```powershell
   uv run python -c "import grid_analysis.domain as m; print(m.__file__)"
   ```

3. Build an `.exe` from `__main__.py` with PyInstaller (the result is in `dist/`):

   ```powershell
   uv run pyinstaller --onefile --name grid_analysis src/grid_analysis/__main__.py
   ```

4. Copy the `.exe` from `dist/` into a folder outside the project and start it there in the terminal. It has to run without the `.venv`.
5. Optional: build the `.exe` with Nuitka and compare size and start-up time:

   ```powershell
   uv run python -m nuitka --standalone --onefile src/grid_analysis/__main__.py
   ```

6. Delete the `.pyd` next to `domain.py` again when you are done. Otherwise it keeps winning over your `.py` file in all further exercises.

## Done when

- [ ] `print(m.__file__)` shows a path ending in `.pyd`
- [ ] `uv run pytest` is green with the `.pyd` in place
- [ ] The `.exe` prints the report from a folder outside the project
- [ ] Neither `.pyd` nor `.exe` nor the folders `build/` and `dist/` show up in `git status`
- [ ] You can explain why a `.pyd` only works with the Python version it was built with

## Hints

- A `.pyd` is loaded exactly like a `.py` file with the same name. If both sit next to each other, the `.pyd` wins.
- A `.pyd` only works with the Python version it was built with. That is the same reason why the `powerfactory` module has a separate folder per Python version.
- PyInstaller bundles interpreter and code without compiling. Simplest option, but the code stays easy to read out.
- Compiling makes reading the code harder but does not prevent it
- Virus scanners like to flag a fresh `.exe`
- In real use, the `.exe` has to find the `powerfactory` module on the target machine

## More

- [Nuitka user manual](https://nuitka.net/user-documentation/user-manual.html)
- [PyInstaller: usage](https://pyinstaller.org/en/stable/usage.html)
- [Cython: building](https://cython.readthedocs.io/en/latest/src/quickstart/build.html)
