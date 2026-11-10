# 💪 R5 Find a vulnerability

**Topic:** Snyk in practice

One dependency of the project has a known vulnerability. You find it with Snyk and update it with uv.

Prerequisite: the [Snyk CLI](https://docs.snyk.io/developer-tools/snyk-cli) is installed and connected to your account (`snyk auth`, opens the browser for sign-in).

## Task

1. Export the dependencies into a `requirements.txt`:

   ```powershell
   uv export --format requirements-txt > requirements.txt
   ```

2. Run `snyk test --file=requirements.txt` and `snyk code test`
3. One dependency has a known vulnerability: find it. In which version is it fixed?
4. Update it with uv. Check first why uv installs exactly this version: look into `pyproject.toml`.
5. Run the tests afterwards, export again and check with `snyk test` that the finding is gone

## Done when

- [ ] You can name the vulnerable package, the installed version and the version that fixes it
- [ ] `pyproject.toml` no longer pins the vulnerable version
- [ ] `uv.lock` contains a version without the finding
- [ ] `snyk test --file=requirements.txt` no longer reports the vulnerability
- [ ] `uv run pytest` is green

## Hints

- `snyk test` checks the dependencies against a database of known vulnerabilities and names the version from which they are fixed
- `snyk code test` checks your own code for insecure patterns
- Snyk can read `uv.lock` directly only in early access and on the enterprise plan. The safe way is the export to `requirements.txt`, the older, simple format for dependency lists that almost every tool understands.
- Update a package: `uv lock --upgrade-package <package>` lifts it to the newest permitted version in the lock file, `uv sync` installs it
- If `pyproject.toml` forbids the new version, adjust the constraint there: `uv add --dev "<package>>=<version>"`
- `requirements.txt` is generated and listed in `.gitignore`

## More

- [Snyk CLI](https://docs.snyk.io/developer-tools/snyk-cli)
- [Snyk: uv support](https://docs.snyk.io/supported-languages/supported-languages-list/python/cli-support-for-uv)
- [uv: Locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
