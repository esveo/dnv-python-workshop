# Solution R2: Run scenarios in parallel

## Files

| File | Goes to |
| --- | --- |
| `exercises/R2/simulation.py` | same path in the project |

```powershell
uv run python exercises/R2/simulation.py
```

## Measurement

Measured on a laptop with 10 cores. Your numbers will differ, the shape of the curve will not.

| Version | Run time | Speed-up |
| --- | --- | --- |
| Sequential | 6.1 s | 1.0 |
| 1 process | 6.3 s | 1.0 |
| 2 processes | 3.2 s | 1.9 |
| 4 processes | 1.7 s | 3.6 |
| 8 processes | 1.3 s | 4.8 |
| 4 threads | 6.1 s | 1.0 |

## What the numbers say

- One process in a pool is slightly slower than the plain loop: starting the process and sending values back and forth costs time
- Up to four processes the speed-up is almost linear. With eight it flattens: not all cores are equally fast, and the fixed start-up cost of the pool gets a larger share of the shrinking run time. More processes than cores gain nothing at all.
- Threads do not help: `compute` is pure Python, and the GIL lets only one thread at a time execute Python code. Threads pay off when the program waits, e.g. for files or the network.

## Details of the solution

- `pool.map` returns the results in the order of the inputs, no matter which process finishes first. That is why the comparison `results == sequential` holds.
- The pool is started inside `main()`, and `main()` is only called below `if __name__ == "__main__":`. On Windows every new process imports the file. Without the guard, each of them would start a pool again.
- `compute` sits at module level. A function defined inside another function or a `lambda` cannot be sent to another process.
- `compute_all` takes any `Executor`, so the same code runs with processes and threads

## For real PowerFactory use

One PowerFactory instance cannot be shared between processes. Each process would need its own instance, and with it its own licence. What parallelises well is the evaluation after the calculation, once the results are plain data.
