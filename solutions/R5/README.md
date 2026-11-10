# Solution R5: Find a vulnerability

There are no files for this exercise: the result is a changed `pyproject.toml` and `uv.lock` in your project.

## 1. Export and scan

```powershell
uv export --format requirements-txt > requirements.txt
snyk test --file=requirements.txt
```

If Snyk cannot tell which package manager is meant, add `--package-manager=pip`.

## 2. The finding

The vulnerable package is `requests`, installed in version 2.31.0. Snyk reports several findings for it, among them:

| Finding | CVE | Fixed in |
| --- | --- | --- |
| Certificate verification stays switched off for a whole session after one request with `verify=False` | CVE-2024-35195 | 2.32.0 |
| Credentials from `.netrc` can leak to another host through a crafted URL | CVE-2024-47081 | 2.32.4 |

Snyk names the version that fixes all findings at once. The list grows over time: take the version from your own scan, not from this table.

`snyk code test` checks your own code and does not report this finding.

## 3. Why exactly this version?

```toml
[dependency-groups]
dev = [
    ...
    "requests==2.31.0",
    ...
]
```

`==` pins the version. `uv lock --upgrade-package requests` alone therefore changes nothing: uv is not allowed to pick another version.

Pins like this are common in older projects. They made sense once and were then forgotten. `uv tree --invert --package requests` shows who needs a package: here only the project itself, in the group `dev`.

## 4. Update

```powershell
uv add --dev "requests>=2.32.4"
```

That replaces the pin in `pyproject.toml`, updates `uv.lock` and installs the new version. Check:

```powershell
uv tree --package requests
```

Nothing in the project imports `requests`. The cleanest fix would therefore be `uv remove --dev requests`. In a real project that is the first question: do we still need this at all?

## 5. Verify

```powershell
uv run pytest
uv export --format requirements-txt > requirements.txt
snyk test --file=requirements.txt
```

The findings for `requests` are gone. If Snyk now reports something else, e.g. in a package that came in on its own as a dependency of a dependency, the same steps apply: `uv tree --invert --package <package>` shows where it comes from.

## What to take along

- A scan only finds known vulnerabilities. A clean result is a snapshot: tomorrow a new entry may be added to the database.
- That is why the scan belongs into a regular run (CI or a scheduled job), not into a one-off action
- `uv.lock` in Git makes sure that everyone has the same, scanned versions
