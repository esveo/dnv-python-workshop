"""Scenario simulation (solution of exercise R2).

200 independent scenario calculations, sequentially and in parallel.

Usage: uv run python exercises/R2/simulation.py
"""

import math
import time
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor

SCENARIO_COUNT = 200
STEPS_PER_SCENARIO = 300_000


def compute(scenario: int) -> float:
    """Stand-in for a compute-heavy scenario calculation in pure Python."""
    value = 0.0
    for step in range(1, STEPS_PER_SCENARIO):
        value += math.sin(scenario + step) / step
    return value


def compute_all(pool: Executor) -> list[float]:
    """Compute all scenarios in the given pool, in the original order."""
    return list(pool.map(compute, range(SCENARIO_COUNT)))


def main() -> None:
    start = time.perf_counter()
    sequential = [compute(scenario) for scenario in range(SCENARIO_COUNT)]
    sequential_duration_s = time.perf_counter() - start
    print(f"Sequential:   {sequential_duration_s:6.2f} s")

    for worker_count in (1, 2, 4, 8):
        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=worker_count) as pool:
            results = compute_all(pool)
        duration_s = time.perf_counter() - start
        print(
            f"{worker_count} processes:  {duration_s:6.2f} s "
            f"(speed-up {sequential_duration_s / duration_s:.1f}, "
            f"same result: {results == sequential})"
        )

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as thread_pool:
        results = compute_all(thread_pool)
    duration_s = time.perf_counter() - start
    print(
        f"4 threads:    {duration_s:6.2f} s "
        f"(speed-up {sequential_duration_s / duration_s:.1f}, "
        f"same result: {results == sequential})"
    )

    print(f"Checksum: {sum(sequential):.6f}")


if __name__ == "__main__":
    main()
