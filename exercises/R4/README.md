# 💪 R4 Create and resolve a conflict

**Topic:** Git conflicts

A conflict arises when two branches changed the same place. Git cannot decide which version is right. You create such a conflict on purpose and resolve it.

Commit or stash your open changes first (`git status` should be clean).

## Task

1. Create two branches in the exercise repository, both starting from `main`:

   ```powershell
   git switch -c limit-a
   # change, commit
   git switch main
   git switch -c limit-b
   # change, commit
   git switch main
   ```

2. Change the same line in `domain.py` differently on both branches, e.g. the lower voltage limit `MIN_VOLTAGE_PU` (0.94 on `limit-a`, 0.96 on `limit-b`), and commit each
3. Merge first `limit-a`, then `limit-b` into `main`:

   ```powershell
   git merge limit-a
   git merge limit-b
   ```

4. Resolve the conflict: bring the file to the right version, remove the markers, `git add`, `git commit`
5. Run the tests afterwards and look at the history: `git log --oneline --graph`

## Done when

- [ ] `git log --oneline --graph` shows both branches and a merge commit
- [ ] `domain.py` no longer contains any conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- [ ] `git status` is clean
- [ ] `uv run pytest` is green
- [ ] You can explain why the first merge went through without a conflict and the second did not

## Hints

- Git marks the place in the file: between `<<<<<<<` and `=======` is the version of the current branch, between `=======` and `>>>>>>>` the version of the branch being merged
- VS Code offers a view with buttons for this ("Accept Current", "Accept Incoming", "Accept Both")
- Abort a merge: `git merge --abort`
- Always run the tests after resolving. A merge without a conflict can still be wrong in content.

## More

- [Pro Git: Basic Merge Conflicts](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [Learn Git Branching](https://learngitbranching.js.org/)
