"""Voltage band violations per scenario (starting code of exercise 07).

Counts, for 1,000 scenarios x 5,000 nodes, how many nodes per scenario
violate the voltage band. With nested Python loops, and therefore slowly.

Usage: uv run python exercises/07/scenarios.py
"""

import time

import numpy as np
from numpy.typing import NDArray

from grid_analysis.powerfactory_fake import fake_voltages_pu

MIN_VOLTAGE_PU = 0.95
MAX_VOLTAGE_PU = 1.05


def count_violations(voltages_pu: NDArray[np.float64]) -> list[int]:
    """Count the nodes outside the voltage band for every scenario.

    ``voltages_pu`` has the shape (scenarios, nodes).
    """
    result = []
    for scenario in voltages_pu:
        count = 0
        for voltage_pu in scenario:
            if voltage_pu < MIN_VOLTAGE_PU or voltage_pu > MAX_VOLTAGE_PU:
                count += 1
        result.append(count)
    return result


def main() -> None:
    voltages_pu = fake_voltages_pu()
    print(f"Data: {voltages_pu.shape[0]} scenarios x {voltages_pu.shape[1]} nodes")

    start = time.perf_counter()
    violations = count_violations(voltages_pu)
    duration_s = time.perf_counter() - start

    print(f"Loop:  {duration_s:.3f} s")
    print(f"Violations in the first five scenarios: {violations[:5]}")


if __name__ == "__main__":
    main()
