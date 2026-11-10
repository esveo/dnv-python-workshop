# 💪 R2 Run scenarios in parallel

**Topic:** Parallelisation

`exercises/R2/simulation.py` runs 200 independent scenario calculations one after another. Independent calculations can be spread across several CPU cores.

Try it:

```powershell
uv run python exercises/R2/simulation.py
```

## Task

1. Open `exercises/R2/simulation.py` and measure the run time of the sequential version
2. Parallelise the calculations with `ProcessPoolExecutor` from `concurrent.futures`
3. Measure with 1, 2, 4 and 8 processes (`max_workers`). From which point on is it no longer worth it?
4. What happens with `ThreadPoolExecutor`? Why?

## Done when

- [ ] The script computes the 200 scenarios with `ProcessPoolExecutor`
- [ ] The parallel result is identical to the sequential one, including the order
- [ ] The script prints the run time for 1, 2, 4 and 8 processes
- [ ] The start of the pool sits below `if __name__ == "__main__":`
- [ ] You can explain why threads barely help here

## Hints

- `pool.map(function, values)` calls the function for every value, spread across the processes, and returns the results in the original order
- `if __name__ == "__main__":` wraps code that only runs when the file is started directly, not on import. On Windows this is mandatory, because every new process imports the file and would otherwise start new processes again.
- Processes cost start-up time, and data has to be copied between them. More processes than cores gain nothing.
- Python has a lock, the GIL (global interpreter lock), that lets only one thread at a time execute Python code. Threads help when waiting for files or the network, not with pure Python computing.

```py
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(compute, range(200)))
```

## More

- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
