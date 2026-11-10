# 💪 01 Set up a project and push it

**Topic:** Git and project structure with uv

You create your own project from scratch and then fetch the exercise repository that all further exercises run in.

## Part 1 (without AI)

Work in a folder of your own outside this repository, e.g. `C:\git-exercise`.

1. Create a bare repository as the "server" and clone it:

   ```powershell
   git init --bare C:\git-exercise\grid-analysis.git
   cd C:\git-exercise
   git clone C:\git-exercise\grid-analysis.git
   ```

2. Change into the clone (`cd grid-analysis`) and turn it into a project: `uv init --package`
3. Add NumPy (`uv add numpy`) as well as pytest, Ruff and mypy as dev dependencies (`uv add --dev ...`)
4. Look at what changed in `pyproject.toml`
5. Check the `.gitignore` against the rule of thumb: is anything missing?
6. Commit and push. The first push into an empty remote: `git push -u origin main`

## Part 2 (without AI)

1. Clone the exercise repository into a folder of your own:

   ```powershell
   git clone https://github.com/esveo/dnv-python-workshop.git
   cd dnv-python-workshop
   ```

   If you are given a different path in the workshop, use that one.

2. Create the environment: `uv sync`
3. Check that everything works: `uv run python -m grid_analysis` prints a short report
4. Open the folder in VS Code

From here on, all exercises work in this exercise repository.

## Done when

- [ ] `git log` in your own project shows at least one commit, and `git status` reports that the branch is up to date with `origin/main`
- [ ] The `pyproject.toml` of your project lists `numpy` under `dependencies` and `pytest`, `ruff`, `mypy` in the `dev` group
- [ ] `.venv/` did not end up in the repository, `uv.lock` did
- [ ] In the exercise repository, `uv run python -m grid_analysis` prints a report

## Hints

- Rule of thumb for the repository: everything goes in that was written by hand and is needed to recreate the project on another machine. Everything that can be generated automatically, only applies to one machine or is secret gets ignored.
- `git status` shows at any time what has changed and what is staged
- If Git reports "dubious ownership" for a repository on a network drive, `git config --global --add safe.directory <path>` helps
- Never put a bare repository into a synchronised folder (OneDrive, SharePoint): the sync client can corrupt the files in `.git`

## More

- [uv: Projects](https://docs.astral.sh/uv/guides/projects/)
- [uv: Installation](https://docs.astral.sh/uv/getting-started/installation/)
- [src layout vs. flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Pro Git: Git on the Server](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server)
