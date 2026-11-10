# Solution R4: Create and resolve a conflict

There are no files for this exercise, only commands.

## The commands

```powershell
git status                      # has to be clean

git switch -c limit-a
# in src/grid_analysis/domain.py: MIN_VOLTAGE_PU = 0.94
git commit -am "Lower voltage limit to 0.94"

git switch main
git switch -c limit-b
# in src/grid_analysis/domain.py: MIN_VOLTAGE_PU = 0.96
git commit -am "Raise voltage limit to 0.96"

git switch main
git merge limit-a               # goes through
git merge limit-b               # conflict
```

## Why only the second merge conflicts

At the first merge, `main` has not changed since `limit-a` branched off. Git just moves `main` forward to the commit of `limit-a` ("fast-forward"), there is nothing to combine.

At the second merge, `main` contains 0.94 and `limit-b` contains 0.96, and both changed the same line starting from 0.95. Git cannot know which one is meant.

## The conflict

```txt
Auto-merging src/grid_analysis/domain.py
CONFLICT (content): Merge conflict in src/grid_analysis/domain.py
Automatic merge failed; fix conflicts and then commit the result.
```

In the file:

```py
<<<<<<< HEAD
MIN_VOLTAGE_PU = 0.94
=======
MIN_VOLTAGE_PU = 0.96
>>>>>>> limit-b
```

`HEAD` is the current branch (`main`, which already contains `limit-a`), below the separator is the version of `limit-b`.

## Resolving

Decide which value is right. That is a question about the domain, not about Git. Then leave exactly one line and remove all three markers:

```py
MIN_VOLTAGE_PU = 0.95
```

```powershell
git add src/grid_analysis/domain.py
git commit                      # Git suggests a message for the merge
uv run pytest
git log --oneline --graph
```

The history then looks roughly like this:

```txt
*   3f2a1c9 Merge branch 'limit-b'
|\
| * 8d41e02 Raise voltage limit to 0.96
* | 51b7a6e Lower voltage limit to 0.94
|/
* a1c93f0 ...
```

## What the tests show

With 0.94 or 0.96 the tests from exercise 03 that check the limit 0.95 go red. That is the point of running them after every merge: Git only checks whether the text fits together, not whether the result is right.

## Clean up

```powershell
git branch -d limit-a limit-b
```

To undo the whole exercise: `git reset --hard <commit before the first merge>`. Careful: that discards everything after that commit.
