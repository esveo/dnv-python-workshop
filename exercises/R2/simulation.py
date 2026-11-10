"""Scenario simulation (starting code of exercise R2).

200 independent scenario calculations run one after another.

Usage: uv run python exercises/R2/simulation.py
"""

import math
import time

SCENARIO_COUNT = 200
STEPS_PER_SCENARIO = 300_000


def compute(scenario: int) -> float:
    """Stand-in for a compute-heavy scenario calculation in pure Python."""
    value = 0.0
    for step in range(1, STEPS_PER_SCENARIO):
        value += math.sin(scenario + step) / step
    return value


def main() -> None:
    start = time.perf_counter()
    results = [compute(scenario) for scenario in range(SCENARIO_COUNT)]
    duration_s = time.perf_counter() - start

    print(f"Sequential: {duration_s:.2f} s for {len(results)} scenarios")
    print(f"Checksum: {sum(results):.6f}")


if __name__ == "__main__":
    main()
