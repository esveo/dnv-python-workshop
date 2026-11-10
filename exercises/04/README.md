# 💪 04 AI writes tests, you review them

**Topic:** Unit tests

Now Copilot writes the tests. Your job is the review: are the tests any good?

## Part 1

1. Let Copilot write tests in the chat for `overloaded_lines(lines, limit_percent)` from `domain.py` and add them to `tests/test_domain.py`
2. Review:
   - Do the tests check behaviour, or do they merely rebuild the implementation?
   - Are edge cases missing? Think of: empty list, exactly on the limit, all overloaded, none overloaded, order of the result
   - Do you understand every test? Do not adopt anything you cannot explain.

## Part 2

1. Deliberately put a bug into the function, e.g. `>` instead of `>=`. Do the tests catch it?
2. Add the missing tests yourself until the bug is caught. Remove the bug again afterwards.
3. Show the coverage:

   ```powershell
   uv run pytest --cov=grid_analysis --cov-report=term-missing
   ```

   Which lines are untested? Which of them matter for the domain?

## Done when

- [ ] `tests/test_domain.py` contains tests for `overloaded_lines`
- [ ] There is a test for a line exactly on the limit
- [ ] There is a test for the empty list
- [ ] With `>` instead of `>=` in `overloaded_lines`, at least one test fails
- [ ] The deliberate bug is removed again, `uv run pytest` is green
- [ ] You can say which untested lines the coverage report shows

## Hints

- Are my tests any good? Deliberately put a bug into the code: at least one test has to fail.
- Coverage shows untested places. 100 % does not mean free of bugs.
- A test that contains the same formula as the implementation does not find errors in the formula. Better: fixed inputs, expectation worked out by hand.

## More

- [Stop Vibe Coding Your Unit Tests](https://www.andy-gallagher.com/blog/stop-vibe-coding-your-unit-tests/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
